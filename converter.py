#!/usr/bin/env python3
"""
PDF Quotation to CSV Converter
Converts PDF quotation files to standardized CSV format
"""

import pdfplumber
import pandas as pd
import re
import sys
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class QuotationConverter:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.header_info = {}
        self.items = []
        self.nre_items = []
    
    def format_date_to_iso(self, date_str: str) -> str:
        """Convert date string to yyyy-mm-dd format"""
        if not date_str:
            return ''
        
        # Try different date formats commonly found in PDFs
        date_formats = [
            '%b. %d, %Y',      # Dec. 22, 2025
            '%B. %d, %Y',      # December. 22, 2025
            '%b %d, %Y',       # Dec 22, 2025
            '%B %d, %Y',       # December 22, 2025
            '%m/%d/%Y',        # 12/22/2025
            '%d/%m/%Y',        # 22/12/2025
            '%Y-%m-%d',        # Already in correct format
        ]
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str.strip(), date_format)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If no format matches, return original
        return date_str
        
    def extract_header_info(self, page) -> Dict[str, str]:
        """Extract header information (To, From, Date, Ref)"""
        text = page.extract_text()
        lines = text.split('\n')
        
        header = {}
        for line in lines:
            if line.startswith('To:'):
                header['customer'] = line.replace('To:', '').strip()
            elif 'From:' in line:
                header['planner'] = line.split('From:')[1].strip()
            elif 'Date:' in line:
                date_str = line.split('Date:')[1].strip()
                # Convert to yyyy-mm-dd format
                header['date'] = self.format_date_to_iso(date_str)
            elif 'Ref:' in line:
                header['ref'] = line.split('Ref:')[1].strip()
                
        return header
    
    def parse_product_field(self, product_text: str) -> Tuple[str, str, str, str]:
        """
        Parse Product field into:
        - Product name (line before Rated Current)
        - Rated Current
        - Cable Length
        - Description (lines after Cable Length)
        """
        if not product_text or product_text.strip() == '':
            return '', '', '', ''
        
        lines = product_text.strip().split('\n')
        product_name = ''
        rated_current = ''
        cable_length = ''
        description_parts = []
        
        found_rated = False
        found_cable = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check for Rated Current
            if 'Rated Current:' in line or 'rated current:' in line.lower():
                rated_current = re.sub(r'.*[Rr]ated [Cc]urrent:\s*', '', line).strip()
                found_rated = True
                # Product name is everything before this line
                if i > 0 and not product_name:
                    product_name = '\n'.join(lines[:i]).strip()
                continue
            
            # Check for Cable Length
            if 'Cable Length:' in line or 'cable length:' in line.lower():
                cable_length = re.sub(r'.*[Cc]able [Ll]ength:\s*', '', line).strip()
                found_cable = True
                continue
            
            # After Cable Length, everything is description
            if found_cable:
                if line.startswith('-'):
                    line = line[1:].strip()
                description_parts.append(line)
            # Before Rated Current, it's product name
            elif not found_rated and not product_name:
                if not line.startswith('-'):
                    product_name = line
        
        description = '\n'.join(description_parts).strip()
        
        # If no product name found, use first line
        if not product_name and lines:
            product_name = lines[0].strip()
            if product_name.startswith('-'):
                product_name = product_name[1:].strip()
        
        return product_name, rated_current, cable_length, description
    
    def extract_table_data(self, page) -> List[Dict]:
        """Extract main quotation table data"""
        tables = page.extract_tables()
        
        if not tables:
            return []
        
        items = []
        main_table = None
        has_header = False
        
        # Find main table (has columns: Item, Product, Delivery Term, MOQ, Unit Price, L/T, Remark)
        for table in tables:
            if table and len(table) > 0:
                header_row = table[0]
                header_str = str(header_row)
                
                # Check if it's a proper header row
                if 'Product' in header_str and 'MOQ' in header_str:
                    main_table = table
                    has_header = True
                    break
                
                # Check if it's a continuation table (no header but has quotation data)
                # Heuristic: 6-8 columns (flexible), has price with $, numeric MOQ
                if 6 <= len(table[0]) <= 8:
                    # Check if looks like quotation data (has $ in price column)
                    first_row = table[0]
                    # Check if column 4 (price) has $ and column 3 (MOQ) is numeric-like
                    has_price = any('$' in str(cell) for cell in first_row if cell)
                    # Improved numeric detection - check non-empty after cleanup
                    has_numeric = any(
                        len(str(cell).replace(',', '').replace('.', '').strip()) > 0 and
                        str(cell).replace(',', '').replace('.', '').strip().isdigit()
                        for cell in first_row if cell and str(cell).strip()
                    )
                    
                    if has_price and has_numeric:
                        main_table = table
                        has_header = False
                        break
        
        if not main_table:
            return []
        
        # Find column indices
        col_indices = {}
        start_row = 0
        
        if has_header:
            # Parse header to find column indices
            header = main_table[0]
            for i, cell in enumerate(header):
                if cell:
                    cell_lower = str(cell).lower().strip()
                    if 'item' in cell_lower:
                        col_indices['item'] = i
                    elif 'product' in cell_lower:
                        col_indices['product'] = i
                    elif 'delivery' in cell_lower:
                        col_indices['delivery_term'] = i
                    elif 'moq' in cell_lower:
                        col_indices['moq'] = i
                    elif 'unit price' in cell_lower or 'price' in cell_lower:
                        col_indices['price'] = i
                    elif 'l/t' in cell_lower:
                        col_indices['lt'] = i
                    elif 'remark' in cell_lower:
                        col_indices['remark'] = i
            start_row = 1
        else:
            # Continuation table without header - assume standard column order
            # Item, Product, Delivery Term, MOQ, Unit Price, L/T, Remark
            col_indices = {
                'item': 0,
                'product': 1,
                'delivery_term': 2,
                'moq': 3,
                'price': 4,
                'lt': 5,
                'remark': 6
            }
            start_row = 0
        
        # Parse data rows
        current_item = None
        current_product = ''
        current_delivery = ''
        current_moq = ''
        current_lt = ''
        current_remark = ''
        
        for row in main_table[start_row:]:
            if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                continue
            
            item_num = row[col_indices.get('item', 0)] if 'item' in col_indices else ''
            product = row[col_indices.get('product', 1)] if 'product' in col_indices else ''
            delivery = row[col_indices.get('delivery_term', 2)] if 'delivery_term' in col_indices else ''
            moq = row[col_indices.get('moq', 3)] if 'moq' in col_indices else ''
            price = row[col_indices.get('price', 4)] if 'price' in col_indices else ''
            lt = row[col_indices.get('lt', 5)] if 'lt' in col_indices else ''
            remark = row[col_indices.get('remark', 6)] if 'remark' in col_indices else ''
            
            # Update current values if not empty (for merged cells)
            if item_num and str(item_num).strip():
                current_item = str(item_num).strip()
            if product and str(product).strip():
                current_product = str(product).strip()
            if delivery and str(delivery).strip():
                current_delivery = str(delivery).strip()
            if moq and str(moq).strip():
                current_moq = str(moq).strip()
            if lt and str(lt).strip():
                current_lt = str(lt).strip()
            if remark and str(remark).strip():
                current_remark = str(remark).strip()
            
            # Add row if there's price data (indicates a valid row)
            if price and str(price).strip():
                items.append({
                    'item': current_item,
                    'product': current_product,
                    'delivery_term': current_delivery,
                    'moq': current_moq,
                    'price': str(price).strip(),
                    'lt': current_lt,
                    'remark': current_remark
                })
        
        return items
    
    def extract_nre_list(self, page) -> List[Dict]:
        """Extract NRE List items
        Requirements:
        - Product = Description field
        - Description = Cavity info
        - Delivery Term = "NRE List"
        - MOQ = Qty value
        - Price = Unit Price (not Amount)
        """
        text = page.extract_text()
        
        if 'NRE List' not in text and 'NRE' not in text:
            return []
        
        tables = page.extract_tables()
        nre_items = []
        
        for table in tables:
            if table and len(table) > 0:
                header_row = table[0]
                # Check if this is NRE List table (has Cavity or Description columns)
                header_str = ' '.join([str(cell) for cell in header_row if cell])
                if 'Cavity' in header_str or ('Description' in header_str and 'Qty' in header_str):
                    # Find column indices
                    col_indices = {}
                    for i, cell in enumerate(header_row):
                        if cell:
                            cell_lower = str(cell).lower().strip()
                            if 'description' in cell_lower:
                                col_indices['description'] = i
                            elif 'cavity' in cell_lower:
                                col_indices['cavity'] = i
                            elif 'qty' in cell_lower and 'unit' not in cell_lower:
                                col_indices['qty'] = i
                            elif 'unit price' in cell_lower:
                                col_indices['unit_price'] = i
                            elif 'amount' in cell_lower:
                                col_indices['amount'] = i
                            elif 'l/t' in cell_lower:
                                col_indices['lt'] = i
                            elif 'remark' in cell_lower:
                                col_indices['remark'] = i
                    
                    # Parse NRE data rows
                    for row in table[1:]:
                        if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                            continue
                        
                        description = row[col_indices.get('description', 0)] if 'description' in col_indices else ''
                        cavity = row[col_indices.get('cavity', 1)] if 'cavity' in col_indices else ''
                        qty = row[col_indices.get('qty', 2)] if 'qty' in col_indices else ''
                        unit_price = row[col_indices.get('unit_price', 3)] if 'unit_price' in col_indices else ''
                        lt = row[col_indices.get('lt', -2)] if 'lt' in col_indices else ''
                        remark = row[col_indices.get('remark', -1)] if 'remark' in col_indices else ''
                        
                        # Only add if description exists
                        if description and str(description).strip():
                            # Combine description with cavity in description field
                            desc_text = str(description).strip()
                            if cavity and str(cavity).strip():
                                desc_text = f"{desc_text}\nCavity: {str(cavity).strip()}"
                            
                            nre_items.append({
                                'product': str(description).strip(),  # Product = Description
                                'description': desc_text,  # Description includes Cavity
                                'qty': str(qty).strip() if qty else '',  # MOQ = Qty
                                'price': str(unit_price).strip() if unit_price else '',  # Only Unit Price
                                'lt': str(lt).strip() if lt else '',
                                'remark': str(remark).strip() if remark else ''
                            })
        
        return nre_items
        
        return nre_items
    
    def convert(self, verbose=False) -> pd.DataFrame:
        """Main conversion function"""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                # Extract header info from first page
                if not self.header_info:
                    self.header_info = self.extract_header_info(page)
                
                # Extract table data
                items = self.extract_table_data(page)
                if verbose:
                    print(f"📄 Page {page.page_number}: Extracted {len(items)} quotation items")
                self.items.extend(items)
                
                # Extract NRE List
                nre_items = self.extract_nre_list(page)
                if verbose and nre_items:
                    print(f"📄 Page {page.page_number}: Extracted {len(nre_items)} NRE items")
                self.nre_items.extend(nre_items)
        
        # Convert to CSV format
        csv_rows = []
        
        # Process main items
        for item in self.items:
            product_name, rated_current, cable_length, description = self.parse_product_field(item['product'])
            
            moq = item['moq']
            qty_value = moq
            remark = item['remark']
            
            # Handle "Sample" MOQ
            if 'sample' in str(moq).lower():
                qty_value = '1'
                remark = 'Sample'
            
            csv_rows.append({
                'Date': self.header_info.get('date', ''),
                'Customer': self.header_info.get('customer', ''),
                'Planner': self.header_info.get('planner', ''),
                'Product': product_name,
                'Rated Current': rated_current,
                'Cable Length': cable_length,
                'Description': description,
                'Delivery Term': item['delivery_term'].replace('\n', ' '),
                'MOQ': qty_value,
                'Price': item['price'],
                'L/T': item['lt'],
                'Remark': remark
            })
        
        # Process NRE List items
        for nre_item in self.nre_items:
            csv_rows.append({
                'Date': self.header_info.get('date', ''),
                'Customer': self.header_info.get('customer', ''),
                'Planner': self.header_info.get('planner', ''),
                'Product': nre_item['product'],  # Product = Description from NRE
                'Rated Current': '',
                'Cable Length': '',
                'Description': nre_item['description'],  # Description includes Cavity
                'Delivery Term': 'NRE List',  # Fixed value
                'MOQ': nre_item['qty'],  # MOQ = Qty
                'Price': nre_item['price'],  # Unit Price only
                'L/T': nre_item['lt'],
                'Remark': nre_item['remark']
            })
        
        # Create DataFrame
        df = pd.DataFrame(csv_rows)
        
        return df
    
    def save_to_csv(self, output_path: str, verbose=False):
        """Convert PDF and save to CSV"""
        df = self.convert(verbose=verbose)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✅ Conversion complete: {output_path}")
        print(f"📊 Total rows: {len(df)}")
        
        if verbose:
            # Check for blank L/T values
            blank_lt = df[df['L/T'].isna() | (df['L/T'] == '')]
            if len(blank_lt) > 0:
                print(f"⚠️  Warning: {len(blank_lt)} rows have blank L/T")
            else:
                print(f"✅ All L/T values filled")
            
            # Show distribution
            print(f"\n📊 Data summary:")
            print(f"   - 6M items: {len(df[df['Cable Length'] == '6M'])}")
            print(f"   - 7.62M items: {len(df[df['Cable Length'] == '7.62M'])}")
            print(f"   - NRE items: {len(df[df['Delivery Term'] == 'NRE List'])}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python converter.py <input_pdf> <output_csv> [-v|--verbose]")
        print("Example: python converter.py quotation.pdf output.csv")
        print("Example: python converter.py quotation.pdf output.csv --verbose")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_csv = sys.argv[2]
    verbose = len(sys.argv) > 3 and sys.argv[3] in ['-v', '--verbose']
    
    try:
        converter = QuotationConverter(input_pdf)
        converter.save_to_csv(output_csv, verbose=verbose)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()