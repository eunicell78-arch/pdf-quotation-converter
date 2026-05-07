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

ITEM_ONLY_PATTERN = re.compile(r'^\d+\s*$')
PRICE_PATTERN = re.compile(r'\$[\d,]+(?:\.\d+)?')
INCOTERM_PATTERN = re.compile(r'\b(FOB|EXW|CIF|CFR|FCA|DAP)\b', re.IGNORECASE)
TABLE_HEADER_PATTERN = re.compile(r'^(MOQ|L/T|Remark|Item)\b', re.IGNORECASE)
RATED_PATTERN = re.compile(r'[Rr]ated\s+[Cc]urrent\s*:')
CABLE_PATTERN = re.compile(r'[Cc]able\s+[Ll]ength\s*:')
BULLET_PATTERN = re.compile(r'^[-•·–—]\s*')
MAX_KEY_VALUE_LABEL_LENGTH = 40
KEY_VALUE_PATTERN = re.compile(
    r'^[A-Za-z][A-Za-z0-9 /&()-]{1,%d}\s*:\s*\S' % MAX_KEY_VALUE_LABEL_LENGTH
)


def safe_get(row, idx, default='', verbose=False):
    """Safely retrieve row[idx], returning default when idx is out of bounds.

    Negative indices are intentionally not supported to avoid silent
    mis-indexing when a row is shorter than expected.
    """
    if row is None or idx is None:
        return default
    if not (0 <= idx < len(row)):
        if verbose:
            print(f"⚠️  safe_get: index {idx} out of range for row of length {len(row)}, using default {default!r}")
        return default
    return row[idx]


def normalize_lt_value(lt_value) -> str:
    """Normalize L/T values to use a single trailing 'wks' suffix."""
    if lt_value is None:
        return ''

    lt_text = str(lt_value).strip()
    if not lt_text:
        return ''

    base_text = re.sub(r'(?i)\s*(?:wk|wks|week|weeks)\.?\s*$', '', lt_text).strip()
    if not base_text:
        return 'wks'

    return f'{base_text}wks'


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
            line = line.strip()
            # Handle 'To:' and 'From:' on the same line, e.g. 'To: EV Mode From: Sherry Liu'
            if 'To:' in line and 'From:' in line:
                to_part = line.split('To:', 1)[1].split('From:', 1)[0].strip()
                from_part = line.split('From:', 1)[1].strip()
                header['customer'] = to_part
                header['planner'] = from_part
            elif line.startswith('To:'):
                header['customer'] = line.split('To:', 1)[1].strip()
            elif 'From:' in line:
                header['planner'] = line.split('From:', 1)[1].strip()
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
        
        lines = [
            BULLET_PATTERN.sub('', line.strip()).strip()
            for line in product_text.strip().split('\n')
            if line and line.strip()
        ]
        product_name = ''
        rated_current = ''
        cable_length = ''
        description_parts = []
        saw_detail_marker = False

        rated_inline_pattern = re.compile(
            r'(?i)\brated\s+current\s*:\s*(.+?)(?=\s*\bcable\s+length\s*:|$)'
        )
        cable_inline_pattern = re.compile(
            r'(?i)\bcable\s+length\s*:\s*(.+?)(?=\s*\b[A-Za-z][A-Za-z0-9 /&()-]{1,%d}\s*:|$)'
            % MAX_KEY_VALUE_LABEL_LENGTH
        )

        for line in lines:
            rated_match = rated_inline_pattern.search(line)
            cable_match = cable_inline_pattern.search(line)
            has_marker = bool(rated_match or cable_match)

            if rated_match and not rated_current:
                rated_current = rated_match.group(1).strip()
            if cable_match and not cable_length:
                cable_length = cable_match.group(1).strip()

            if has_marker and not product_name:
                marker_starts = [m.start() for m in (rated_match, cable_match) if m]
                if marker_starts:
                    prefix = line[:min(marker_starts)].strip()
                    if prefix:
                        product_name = prefix

            if has_marker:
                saw_detail_marker = True
                continue

            if not product_name:
                product_name = line
                continue

            if saw_detail_marker:
                description_parts.append(line)

        description = '\n'.join(description_parts).strip()

        if not product_name and lines:
            product_name = lines[0].strip()

        return product_name, rated_current, cable_length, description
    
    def extract_table_data(self, page, verbose=False) -> List[Dict]:
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
            
            item_num = safe_get(row, col_indices.get('item', 0), verbose=verbose) if 'item' in col_indices else ''
            product = safe_get(row, col_indices.get('product', 1), verbose=verbose) if 'product' in col_indices else ''
            delivery = safe_get(row, col_indices.get('delivery_term', 2), verbose=verbose) if 'delivery_term' in col_indices else ''
            moq = safe_get(row, col_indices.get('moq', 3), verbose=verbose) if 'moq' in col_indices else ''
            price = safe_get(row, col_indices.get('price', 4), verbose=verbose) if 'price' in col_indices else ''
            lt = safe_get(row, col_indices.get('lt', 5), verbose=verbose) if 'lt' in col_indices else ''
            remark = safe_get(row, col_indices.get('remark', 6), verbose=verbose) if 'remark' in col_indices else ''
            
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
        
        # Supplement items whose product cell is missing small-font detail lines
        items = self._supplement_product_from_page_text(page, items)

        return items

    def _supplement_product_from_page_text(self, page, items) -> List[Dict]:
        """Fallback: recover small-font product detail lines missed by table extraction.

        Some PDFs render detail lines (Rated Current, Cable Length, description
        bullets) in a smaller font inside the Product cell.  pdfplumber's table
        extraction can miss those lines, while page-level text extraction usually
        captures them.

        For each item whose 'product' text appears to be a bare product name (i.e.
        has no 'Rated Current' or 'Cable Length' keywords), this method searches
        the full page text for that product name and collects nearby detail lines
        that immediately follow it. The item's 'product' value is replaced only
        when richer detail text is actually found.

        Already-complete items (detail lines already present) are returned unchanged.
        """
        if not items:
            return items

        def _is_incomplete(product_text):
            if not product_text:
                return False
            lower = product_text.lower()
            return 'rated current' not in lower or 'cable length' not in lower

        # Quick exit when nothing needs supplementing
        if not any(_is_incomplete(item['product']) for item in items):
            return items

        page_text = page.extract_text() or ''
        if not page_text:
            return items

        page_lines = [ln.strip() for ln in page_text.split('\n') if ln.strip()]
        def _is_boundary_line(line: str) -> bool:
            """Return True when a line clearly belongs to another table section/row."""
            return (
                ITEM_ONLY_PATTERN.match(line)
                or PRICE_PATTERN.search(line)
                or INCOTERM_PATTERN.search(line)
                or TABLE_HEADER_PATTERN.match(line)
            )

        def _is_detail_cue(line: str) -> bool:
            """Return True when a line looks like product detail text."""
            if not line:
                return False
            return (
                RATED_PATTERN.search(line)
                or CABLE_PATTERN.search(line)
                or BULLET_PATTERN.match(line)
            )

        result = []
        for item in items:
            if not _is_incomplete(item['product']):
                result.append(item)
                continue

            product_name = (item['product'] or '').strip()
            if not product_name:
                result.append(item)
                continue

            # Locate the product name in the page text lines
            product_lower = product_name.lower()
            start_idx = None
            for idx, pl in enumerate(page_lines):
                if pl.lower() == product_lower or product_lower in pl.lower():
                    start_idx = idx
                    break

            if start_idx is None:
                result.append(item)
                continue

            # Build enriched product text: use the known-good product name as
            # the first line, then append detail lines from nearby page text.
            enriched_lines = [product_name]
            in_detail_section = False
            for pl in page_lines[start_idx + 1:]:
                if _is_boundary_line(pl):
                    break

                if _is_detail_cue(pl):
                    enriched_lines.append(pl)
                    in_detail_section = True
                else:
                    if in_detail_section:
                        # Keep follow-up narrative lines after details start
                        enriched_lines.append(pl)
                    elif KEY_VALUE_PATTERN.match(pl):
                        # Preserve key/value detail lines even without a leading bullet
                        enriched_lines.append(pl)
                        in_detail_section = True
                    else:
                        # Ignore unrelated text before details begin.
                        continue

                if len(enriched_lines) > 10:  # safety cap
                    break

            enriched_text = '\n'.join(enriched_lines)

            # Only upgrade the item when the enriched text actually contains
            # recognisable detail lines; otherwise leave the original unchanged.
            if (re.search(r'[Rr]ated\s+[Cc]urrent\s*:', enriched_text)
                    or re.search(r'[Cc]able\s+[Ll]ength\s*:', enriched_text)):
                item = dict(item)
                item['product'] = enriched_text

            result.append(item)

        return result

    def extract_nre_list(self, page, verbose=False) -> List[Dict]:
        """Extract NRE List items
        Requirements:
        - Product = Description field
        - Description = Description text combined with Cavity info (if present)
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
                        
                        description = safe_get(row, col_indices.get('description', 0), verbose=verbose) if 'description' in col_indices else ''
                        cavity = safe_get(row, col_indices.get('cavity', 1), verbose=verbose) if 'cavity' in col_indices else ''
                        qty = safe_get(row, col_indices.get('qty', 2), verbose=verbose) if 'qty' in col_indices else ''
                        unit_price = safe_get(row, col_indices.get('unit_price', 3), verbose=verbose) if 'unit_price' in col_indices else ''
                        lt = safe_get(row, col_indices.get('lt', 4), verbose=verbose) if 'lt' in col_indices else ''
                        remark = safe_get(row, col_indices.get('remark', 5), verbose=verbose) if 'remark' in col_indices else ''
                        
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
    
    def convert(self, verbose=False) -> pd.DataFrame:
        """Main conversion function"""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                # Extract header info from first page
                if not self.header_info:
                    self.header_info = self.extract_header_info(page)
                
                # Extract table data
                items = self.extract_table_data(page, verbose=verbose)
                if verbose:
                    print(f"📄 Page {page.page_number}: Extracted {len(items)} quotation items")
                self.items.extend(items)
                
                # Extract NRE List
                nre_items = self.extract_nre_list(page, verbose=verbose)
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
                'L/T': normalize_lt_value(item['lt']),
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
                'L/T': normalize_lt_value(nre_item['lt']),
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
