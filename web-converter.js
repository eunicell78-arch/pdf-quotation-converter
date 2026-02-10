// PDF.js worker configuration
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

let selectedFile = null;

// File selection and drag-drop handlers
document.getElementById('pdfFileInput').addEventListener('change', handleFileSelect);

const dropZone = document.getElementById('dropZone');
dropZone.addEventListener('click', () => document.getElementById('pdfFileInput').click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('dragleave', handleDragLeave);
dropZone.addEventListener('drop', handleDrop);

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        selectedFile = file;
        displayFileInfo(file);
    } else {
        alert('PDF 파일만 선택할 수 있습니다.');
    }
}

function handleDragOver(event) {
    event.preventDefault();
    dropZone.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.preventDefault();
    dropZone.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    dropZone.classList.remove('drag-over');
    
    const file = event.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        selectedFile = file;
        displayFileInfo(file);
    } else {
        alert('PDF 파일만 선택할 수 있습니다.');
    }
}

function displayFileInfo(file) {
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    document.getElementById('fileInfo').style.display = 'block';
    document.getElementById('convertBtn').disabled = false;
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

function removeFile() {
    selectedFile = null;
    document.getElementById('pdfFileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('convertBtn').disabled = true;
}

function resetConverter() {
    removeFile();
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('dropZone').style.display = 'block';
    document.getElementById('convertBtn').style.display = 'block';
}

// Main conversion function
async function convertPDF() {
    if (!selectedFile) {
        alert('먼저 PDF 파일을 선택해주세요.');
        return;
    }

    // Hide upload UI and show progress
    document.getElementById('dropZone').style.display = 'none';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('convertBtn').style.display = 'none';
    document.getElementById('progressSection').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';

    try {
        updateProgress(10, 'PDF 파일 로딩 중...');

        // Load PDF
        const arrayBuffer = await selectedFile.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        
        updateProgress(30, 'PDF 텍스트 추출 중...');

        // Extract data from all pages
        let headerInfo = {};
        let items = [];
        let nreItems = [];

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(' ');

            // Extract header info from first page
            if (pageNum === 1 && Object.keys(headerInfo).length === 0) {
                headerInfo = extractHeaderInfo(pageText);
            }

            // Try to extract table data
            const pageItems = await extractTableData(page, textContent);
            items = items.concat(pageItems);

            updateProgress(30 + (pageNum / pdf.numPages) * 40, `페이지 ${pageNum}/${pdf.numPages} 처리 중...`);
        }

        updateProgress(80, 'CSV 생성 중...');

        // Check if any data was extracted
        if (items.length === 0) {
            console.warn('No items extracted from PDF');
            throw new Error('PDF에서 데이터를 추출할 수 없습니다. 파일이 올바른 견적서 형식인지 확인해주세요.\n\n데스크톱 버전(converter.py)을 사용하면 더 정확한 변환이 가능합니다.');
        }

        console.log(`Total items extracted: ${items.length}`);

        // Convert to CSV
        const csv = generateCSV(headerInfo, items, nreItems);

        updateProgress(90, 'CSV 다운로드 준비 중...');

        // Download CSV
        downloadCSV(csv, selectedFile.name.replace('.pdf', '.csv'));

        updateProgress(100, '완료!');

        // Show success
        setTimeout(() => {
            document.getElementById('progressSection').style.display = 'none';
            document.getElementById('resultSection').style.display = 'block';
            document.getElementById('resultMessage').textContent = 
                `CSV 파일이 생성되었습니다: ${selectedFile.name.replace('.pdf', '.csv')}`;
        }, 500);

    } catch (error) {
        console.error('Conversion error:', error);
        document.getElementById('progressSection').style.display = 'none';
        document.getElementById('errorSection').style.display = 'block';
        document.getElementById('errorMessage').textContent = 
            `오류: ${error.message}\n\n파일이 올바른 견적서 형식인지 확인해주세요.`;
    }
}

function updateProgress(percent, message) {
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('statusText').textContent = message;
}

// Extract header information
function extractHeaderInfo(text) {
    const header = {};
    const lines = text.split(/[\n\r]+/);
    
    for (const line of lines) {
        if (line.includes('To:')) {
            header.customer = line.split('To:')[1].trim();
        } else if (line.includes('From:')) {
            header.planner = line.split('From:')[1].trim();
        } else if (line.includes('Date:')) {
            header.date = line.split('Date:')[1].trim();
        } else if (line.includes('Ref:')) {
            header.ref = line.split('Ref:')[1].trim();
        }
    }
    
    return header;
}

// Extract table data from page
async function extractTableData(page, textContent) {
    const items = [];
    
    console.log('=== Starting table extraction ===');
    console.log('Total text items:', textContent.items.length);
    
    // Group text items by vertical position (Y coordinate) to form rows
    const rowMap = new Map();
    const yTolerance = 5; // Increased tolerance for grouping items in same row
    
    // Organize text items by row (Y position)
    for (const item of textContent.items) {
        if (!item.str || item.str.trim() === '') continue; // Skip empty items
        
        const y = Math.round(item.transform[5] / yTolerance) * yTolerance;
        if (!rowMap.has(y)) {
            rowMap.set(y, []);
        }
        rowMap.get(y).push({
            text: item.str.trim(),
            x: item.transform[4],
            y: item.transform[5],
            width: item.width
        });
    }
    
    console.log('Grouped into', rowMap.size, 'rows');
    
    // Sort rows by Y position (top to bottom)
    const rows = Array.from(rowMap.entries())
        .sort((a, b) => b[0] - a[0])
        .map(([y, items]) => {
            // Sort items in each row by X position (left to right)
            return items.sort((a, b) => a.x - b.x);
        });
    
    // Find header row containing "Product" and "MOQ" (case-insensitive)
    let headerRowIndex = -1;
    let headerRow = null;
    
    for (let i = 0; i < rows.length; i++) {
        const rowText = rows[i].map(item => item.text).join(' ').toLowerCase();
        if (rowText.includes('product') && rowText.includes('moq')) {
            headerRowIndex = i;
            headerRow = rows[i];
            console.log('Found header at row', i, ':', rows[i].map(item => item.text).join(' | '));
            break;
        }
    }
    
    if (headerRowIndex === -1) {
        console.warn('❌ No table header found with Product and MOQ columns');
        console.log('First 5 rows:');
        for (let i = 0; i < Math.min(5, rows.length); i++) {
            console.log(`Row ${i}:`, rows[i].map(item => item.text).join(' | '));
        }
        return items;
    }
    
    // Determine column boundaries based on header
    const columns = {
        item: null,
        product: null,
        delivery_term: null,
        moq: null,
        price: null,
        lt: null,
        remark: null
    };
    
    // Map header text to column positions
    for (let i = 0; i < headerRow.length; i++) {
        const text = headerRow[i].text.toLowerCase();
        const x = headerRow[i].x;
        
        if (text.includes('item') && !columns.item) {
            columns.item = { index: i, x: x, text: headerRow[i].text };
        } else if (text.includes('product')) {
            columns.product = { index: i, x: x, text: headerRow[i].text };
        } else if (text.includes('delivery')) {
            columns.delivery_term = { index: i, x: x, text: headerRow[i].text };
        } else if (text.includes('moq')) {
            columns.moq = { index: i, x: x, text: headerRow[i].text };
        } else if (text.includes('price') || text.includes('unit')) {
            columns.price = { index: i, x: x, text: headerRow[i].text };
        } else if (text.includes('l/t') || text.includes('lead')) {
            columns.lt = { index: i, x: x, text: headerRow[i].text };
        } else if (text.includes('remark') || text.includes('note')) {
            columns.remark = { index: i, x: x, text: headerRow[i].text };
        }
    }
    
    console.log('✅ Detected columns:', JSON.stringify(columns, null, 2));
    
    // Extract data rows (after header)
    let currentItem = null;
    let currentProduct = '';
    let currentDelivery = '';
    
    for (let i = headerRowIndex + 1; i < rows.length; i++) {
        const row = rows[i];
        if (row.length === 0) continue;
        
        // Build row data by mapping to columns
        const rowData = {
            item: '',
            product: '',
            delivery_term: '',
            moq: '',
            price: '',
            lt: '',
            remark: ''
        };
        
        // Assign text items to columns based on X position
        for (const textItem of row) {
            const x = textItem.x;
            const text = textItem.text;
            
            // Find which column this text belongs to
            let closestColumn = null;
            let minDistance = Infinity;
            
            for (const [colName, colInfo] of Object.entries(columns)) {
                if (colInfo && colInfo.x !== undefined) {
                    const distance = Math.abs(x - colInfo.x);
                    if (distance < minDistance && distance < 100) { // 100 point tolerance
                        minDistance = distance;
                        closestColumn = colName;
                    }
                }
            }
            
            if (closestColumn) {
                rowData[closestColumn] += (rowData[closestColumn] ? ' ' : '') + text;
            }
        }
        
        // Update current values for merged cells
        if (rowData.item && rowData.item.trim()) {
            currentItem = rowData.item.trim();
        }
        if (rowData.product && rowData.product.trim()) {
            currentProduct = rowData.product.trim();
        }
        if (rowData.delivery_term && rowData.delivery_term.trim()) {
            currentDelivery = rowData.delivery_term.trim();
        }
        
        // Only add row if it has MOQ data (indicates a complete row)
        if (rowData.moq && rowData.moq.trim()) {
            items.push({
                item: currentItem || '',
                product: currentProduct || rowData.product || '',
                delivery_term: currentDelivery || rowData.delivery_term || '',
                moq: rowData.moq.trim(),
                price: rowData.price.trim(),
                lt: rowData.lt.trim(),
                remark: rowData.remark.trim()
            });
        }
    }
    
    console.log('Extracted items:', items);
    return items;
}

// Parse product field
function parseProductField(productText) {
    if (!productText || productText.trim() === '') {
        return ['', '', '', ''];
    }
    
    const lines = productText.trim().split('\n');
    let productName = '';
    let ratedCurrent = '';
    let cableLength = '';
    let description = '';
    
    let foundRated = false;
    let foundCable = false;
    const descriptionParts = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (line.match(/rated\s*current/i)) {
            ratedCurrent = line.replace(/.*rated\s*current:\s*/i, '').trim();
            foundRated = true;
            if (i > 0 && !productName) {
                productName = lines.slice(0, i).join('\n').trim();
            }
            continue;
        }
        
        if (line.match(/cable\s*length/i)) {
            cableLength = line.replace(/.*cable\s*length:\s*/i, '').trim();
            foundCable = true;
            continue;
        }
        
        if (foundCable) {
            let cleanLine = line.startsWith('-') ? line.substring(1).trim() : line;
            descriptionParts.push(cleanLine);
        } else if (!foundRated && !productName) {
            if (!line.startsWith('-')) {
                productName = line;
            }
        }
    }
    
    description = descriptionParts.join('\n').trim();
    
    if (!productName && lines.length > 0) {
        productName = lines[0].trim();
        if (productName.startsWith('-')) {
            productName = productName.substring(1).trim();
        }
    }
    
    return [productName, ratedCurrent, cableLength, description];
}

// Generate CSV content
function generateCSV(headerInfo, items, nreItems) {
    const csvRows = [];
    
    // Add header row
    csvRows.push([
        'Date',
        'Customer',
        'Planner',
        'Product',
        'Rated Current',
        'Cable Length',
        'Description',
        'Delivery Term',
        'MOQ',
        'Price',
        'L/T',
        'Remark'
    ]);
    
    // Add main items
    for (const item of items) {
        const [productName, ratedCurrent, cableLength, description] = 
            parseProductField(item.product);
        
        let moqValue = item.moq;
        let remark = item.remark;
        
        if (item.moq && item.moq.toLowerCase().includes('sample')) {
            moqValue = '1';
            remark = 'Sample';
        }
        
        csvRows.push([
            headerInfo.date || '',
            headerInfo.customer || '',
            headerInfo.planner || '',
            productName,
            ratedCurrent,
            cableLength,
            description,
            item.delivery_term || '',
            moqValue,
            item.price || '',
            item.lt || '',
            remark
        ]);
    }
    
    // Add NRE items
    for (const nreItem of nreItems) {
        csvRows.push([
            headerInfo.date || '',
            headerInfo.customer || '',
            headerInfo.planner || '',
            nreItem.product || '',
            '',
            '',
            nreItem.cavity || '',
            'NRE List',
            nreItem.qty || '',
            nreItem.price || '',
            nreItem.lt || '',
            nreItem.remark || ''
        ]);
    }
    
    // Convert to CSV string with UTF-8 BOM for Excel compatibility
    const csvContent = '\uFEFF' + csvRows.map(row => 
        row.map(cell => {
            // Escape quotes and wrap in quotes if needed
            const cellStr = String(cell || '');
            if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n')) {
                return '"' + cellStr.replace(/"/g, '""') + '"';
            }
            return cellStr;
        }).join(',')
    ).join('\n');
    
    return csvContent;
}

// Download CSV file
function downloadCSV(csvContent, filename) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    URL.revokeObjectURL(url);
}
