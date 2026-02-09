#!/usr/bin/env python3
"""
PDF Quotation to CSV Converter - GUI Version
User-friendly GUI interface for converting PDF quotations to CSV
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import threading
from pathlib import Path

# Import the converter module
from converter import QuotationConverter


class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("견적서 변환기 - PDF to CSV Converter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Variables
        self.pdf_path = tk.StringVar()
        self.csv_path = tk.StringVar()
        self.status_text = tk.StringVar(value="대기 중...")
        self.is_converting = False  # Track conversion state
        
        # Set default save directory to Desktop
        desktop = Path.home() / "Desktop"
        if desktop.exists():
            self.default_dir = str(desktop)
        else:
            self.default_dir = str(Path.home())
        
        self.setup_ui()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """Handle window close event"""
        if self.is_converting:
            result = messagebox.askyesno(
                "변환 진행 중",
                "변환이 진행 중입니다. 종료하시면 변환이 중단됩니다.\n정말 종료하시겠습니까?",
                icon='warning'
            )
            if not result:
                return
        
        self.root.destroy()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title Label
        title_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="📄 PDF 견적서 → CSV 변환기",
            font=("맑은 고딕", 18, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # PDF File Selection
        pdf_frame = tk.LabelFrame(content_frame, text="1. PDF 파일 선택", font=("맑은 고딕", 10, "bold"), padx=10, pady=10)
        pdf_frame.pack(fill=tk.X, pady=(0, 15))
        
        pdf_entry = tk.Entry(pdf_frame, textvariable=self.pdf_path, font=("맑은 고딕", 9), state="readonly")
        pdf_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        pdf_button = tk.Button(
            pdf_frame,
            text="파일 선택",
            command=self.select_pdf,
            bg="#4CAF50",
            fg="white",
            font=("맑은 고딕", 9, "bold"),
            width=12,
            cursor="hand2"
        )
        pdf_button.pack(side=tk.RIGHT)
        
        # CSV Save Location
        csv_frame = tk.LabelFrame(content_frame, text="2. 저장 위치 선택", font=("맑은 고딕", 10, "bold"), padx=10, pady=10)
        csv_frame.pack(fill=tk.X, pady=(0, 15))
        
        csv_entry = tk.Entry(csv_frame, textvariable=self.csv_path, font=("맑은 고딕", 9), state="readonly")
        csv_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        csv_button = tk.Button(
            csv_frame,
            text="저장 위치",
            command=self.select_csv,
            bg="#2196F3",
            fg="white",
            font=("맑은 고딕", 9, "bold"),
            width=12,
            cursor="hand2"
        )
        csv_button.pack(side=tk.RIGHT)
        
        # Convert Button
        self.convert_button = tk.Button(
            content_frame,
            text="🚀 변환 시작",
            command=self.start_conversion,
            bg="#FF9800",
            fg="white",
            font=("맑은 고딕", 12, "bold"),
            height=2,
            cursor="hand2"
        )
        self.convert_button.pack(fill=tk.X, pady=(0, 15))
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Status Label
        status_label = tk.Label(
            content_frame,
            textvariable=self.status_text,
            font=("맑은 고딕", 9),
            fg="#666666"
        )
        status_label.pack()
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#f5f5f5", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="💡 Tip: PDF 파일을 선택하고 저장 위치를 지정한 후 변환을 시작하세요",
            font=("맑은 고딕", 8),
            bg="#f5f5f5",
            fg="#888888"
        )
        footer_label.pack(pady=10)
    
    def select_pdf(self):
        """Open file dialog to select PDF file"""
        filename = filedialog.askopenfilename(
            title="PDF 파일 선택",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialdir=self.default_dir
        )
        
        if filename:
            self.pdf_path.set(filename)
            self.status_text.set(f"선택됨: {os.path.basename(filename)}")
            
            # Auto-suggest CSV filename
            if not self.csv_path.get():
                suggested_csv = os.path.splitext(filename)[0] + ".csv"
                self.csv_path.set(suggested_csv)
    
    def select_csv(self):
        """Open file dialog to select CSV save location"""
        initial_file = ""
        if self.pdf_path.get():
            pdf_name = os.path.basename(self.pdf_path.get())
            initial_file = os.path.splitext(pdf_name)[0] + ".csv"
        
        filename = filedialog.asksaveasfilename(
            title="CSV 저장 위치 선택",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=self.default_dir,
            initialfile=initial_file
        )
        
        if filename:
            self.csv_path.set(filename)
            self.status_text.set(f"저장 위치: {os.path.basename(filename)}")
    
    def start_conversion(self):
        """Start the conversion process"""
        pdf_file = self.pdf_path.get()
        csv_file = self.csv_path.get()
        
        # Validation
        if not pdf_file:
            messagebox.showerror("오류", "PDF 파일을 선택해주세요.")
            return
        
        if not csv_file:
            messagebox.showerror("오류", "CSV 저장 위치를 선택해주세요.")
            return
        
        if not os.path.exists(pdf_file):
            messagebox.showerror("오류", f"PDF 파일을 찾을 수 없습니다:\n{pdf_file}")
            return
        
        # Disable button and start progress
        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        self.status_text.set("변환 중...")
        
        # Run conversion in a separate thread to keep GUI responsive
        thread = threading.Thread(target=self.perform_conversion, args=(pdf_file, csv_file))
        thread.daemon = True
        thread.start()
    
    def perform_conversion(self, pdf_file, csv_file):
        """Perform the actual conversion (runs in separate thread)"""
        try:
            # Create converter and convert
            converter = QuotationConverter(pdf_file)
            converter.save_to_csv(csv_file)
            
            # Update UI on success
            self.root.after(0, self.conversion_success, csv_file)
            
        except Exception as e:
            # Update UI on error
            self.root.after(0, self.conversion_error, str(e))
    
    def conversion_success(self, csv_file):
        """Handle successful conversion"""
        self.is_converting = False
        self.progress_bar.stop()
        self.convert_button.config(state=tk.NORMAL)
        self.status_text.set("✅ 변환 완료!")
        
        # Show success message with options
        result = messagebox.askyesno(
            "변환 완료",
            f"CSV 파일이 성공적으로 생성되었습니다!\n\n{csv_file}\n\n파일을 여시겠습니까?",
            icon='info'
        )
        
        if result:
            try:
                # Open the CSV file with default application
                if sys.platform == 'win32':
                    os.startfile(csv_file)
                elif sys.platform == 'darwin':  # macOS
                    os.system(f'open "{csv_file}"')
                else:  # linux
                    os.system(f'xdg-open "{csv_file}"')
            except Exception as e:
                messagebox.showwarning("알림", f"파일을 여는 중 오류가 발생했습니다:\n{e}")
    
    def conversion_error(self, error_message):
        """Handle conversion error"""
        self.is_converting = False
        self.progress_bar.stop()
        self.convert_button.config(state=tk.NORMAL)
        self.status_text.set("❌ 변환 실패")
        
        messagebox.showerror(
            "변환 오류",
            f"PDF 변환 중 오류가 발생했습니다:\n\n{error_message}\n\n파일이 올바른 견적서 형식인지 확인해주세요."
        )


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = ConverterGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
