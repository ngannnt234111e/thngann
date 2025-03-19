import os
import sys
import webbrowser
import pandas as pd
import plotly.express as px
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel,
    QWidget, QFileDialog, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class CurriculumVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chương Trình Đào Tạo Visualizer")
        self.setGeometry(100, 100, 600, 200)

        # Biến lưu trữ đường dẫn file Excel
        self.excel_path = ""

        # Thiết lập giao diện
        self.setup_ui()

    def setup_ui(self):
        # Widget chính và layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Tiêu đề
        self.title_label = QLabel("Chương Trình Đào Tạo Visualizer")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Layout cho việc chọn file
        self.file_layout = QHBoxLayout()

        # Label cho việc chọn file
        self.file_label = QLabel("Choose Dataset:")
        self.file_layout.addWidget(self.file_label)

        # Text box hiển thị đường dẫn file
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_layout.addWidget(self.file_path_edit, 1)

        # Nút browse để chọn file
        self.browse_button = QPushButton("...")
        self.browse_button.setMaximumWidth(40)
        self.browse_button.clicked.connect(self.browse_file)
        self.file_layout.addWidget(self.browse_button)

        # Thêm layout chọn file vào layout chính
        self.main_layout.addLayout(self.file_layout)

        # Layout cho các nút chức năng
        self.button_layout = QHBoxLayout()

        # Nút mở biểu đồ trong trình duyệt
        self.open_button = QPushButton("Open Chart in Browser")
        self.open_button.setMinimumHeight(40)
        self.open_button.clicked.connect(self.open_chart_in_browser)
        self.button_layout.addWidget(self.open_button)

        # Nút lưu biểu đồ thành file HTML
        self.save_button = QPushButton("Save Chart to HTML File")
        self.save_button.setMinimumHeight(40)
        self.save_button.clicked.connect(self.save_chart_to_html)
        self.button_layout.addWidget(self.save_button)

        # Thêm layout nút vào layout chính
        self.main_layout.addLayout(self.button_layout)

    def browse_file(self):
        """Mở hộp thoại chọn file Excel"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            self.excel_path = file_path
            self.file_path_edit.setText(file_path)

    def create_curriculum_data(self, excel_path):
        """Đọc dữ liệu từ file Excel và tạo cấu trúc dữ liệu cho biểu đồ sunburst"""
        try:
            # Đọc dữ liệu từ file Excel
            df = pd.read_excel(excel_path)

            # Đổi tên cột để dễ xử lý
            if len(df.columns) >= 6:
                df.columns = ['TT', 'MaHP', 'TenHP', 'TinChi', 'LoaiHP', 'HocKy']
            else:
                raise ValueError("Excel file does not have the expected columns")

            # Chuyển đổi các cột sang kiểu dữ liệu phù hợp
            df['TT'] = df['TT'].astype('Int64')
            df['TinChi'] = pd.to_numeric(df['TinChi'], errors='coerce').fillna(0).astype('Int64')
            df['HocKy'] = pd.to_numeric(df['HocKy'], errors='coerce').fillna(0).astype('Int64')

            # Đảm bảo không có giá trị NaN
            df['MaHP'] = df['MaHP'].fillna('')
            df['TenHP'] = df['TenHP'].fillna('')
            df['LoaiHP'] = df['LoaiHP'].fillna('')

            # Thêm cột 'id' để định danh duy nhất cho mỗi học phần
            df['id'] = df.apply(lambda row: f"{row['TT']}. {row['TenHP']}", axis=1)

            # Thêm cột 'parent' để xác định mối quan hệ phân cấp
            df['parent'] = df.apply(lambda row: f"Học kỳ {row['HocKy']} - {row['LoaiHP']}", axis=1)

            # Tạo DataFrame cho các học kỳ
            hk_data = []
            for hk in range(1, 11):
                bb_tc = df[(df['HocKy'] == hk) & (df['LoaiHP'] == 'Bắt buộc')]['TinChi'].sum()
                tc_tc = df[(df['HocKy'] == hk) & (df['LoaiHP'] == 'Tự chọn')]['TinChi'].sum()

                # Thêm dòng cho "Bắt buộc"
                if bb_tc > 0:
                    hk_data.append({
                        'id': f"Học kỳ {hk} - Bắt buộc",
                        'parent': f"Học kỳ {hk}",
                        'TenHP': 'Bắt buộc',
                        'TinChi': int(bb_tc)
                    })

                # Thêm dòng cho "Tự chọn"
                if tc_tc > 0:
                    hk_data.append({
                        'id': f"Học kỳ {hk} - Tự chọn",
                        'parent': f"Học kỳ {hk}",
                        'TenHP': 'Tự chọn',
                        'TinChi': int(tc_tc)
                    })

                # Thêm dòng cho học kỳ
                total_tc = int(bb_tc + tc_tc)
                hk_data.append({
                    'id': f"Học kỳ {hk}",
                    'parent': "Chương trình đào tạo",
                    'TenHP': f"Học kỳ {hk}",
                    'TinChi': total_tc
                })

            # Tạo DataFrame cho các học kỳ
            hk_df = pd.DataFrame(hk_data)

            # Thêm dòng gốc "Chương trình đào tạo"
            root_df = pd.DataFrame([{
                'id': "Chương trình đào tạo",
                'parent': "",
                'TenHP': "Chương trình đào tạo",
                'TinChi': int(df['TinChi'].sum())
            }])

            # Kết hợp các DataFrame
            result_df = pd.concat([
                root_df,
                hk_df,
                df[['id', 'parent', 'TenHP', 'TinChi']]
            ], ignore_index=True)

            return result_df

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing Excel file: {str(e)}")
            return None

    def create_sunburst_chart(self, df):
        """Tạo biểu đồ sunburst từ DataFrame"""
        try:
            # Tạo biểu đồ sunburst với màu sắc mới
            # Thay đổi bảng màu từ Plotly sang Viridis
            fig = px.sunburst(
                df,
                ids='id',
                parents='parent',
                names='TenHP',
                values='TinChi',
                title='Chương Trình Đào Tạo Ngành Công Nghệ Thông Tin',
                color_discrete_sequence=px.colors.sequential.Viridis,  # Thay đổi bảng màu ở đây
                branchvalues='total'
            )

            # Tùy chỉnh biểu đồ
            fig.update_layout(
                margin=dict(t=30, l=0, r=0, b=0),
                font=dict(size=14, family="Arial, sans-serif"),
                height=800,
                width=1000,
                title_font_size=24,
                title_x=0.5,
                template="plotly_white"
            )

            # Tùy chỉnh hover info
            fig.update_traces(
                hovertemplate='<b>%{label}</b><br>Số tín chỉ: %{value}<br><extra></extra>',
                textinfo='label+value'
            )

            return fig

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error creating chart: {str(e)}")
            return None

    def open_chart_in_browser(self):
        """Mở biểu đồ trong trình duyệt"""
        if not self.excel_path:
            QMessageBox.warning(self, "Warning", "Please select an Excel file first.")
            return

        try:
            # Tạo dữ liệu
            df = self.create_curriculum_data(self.excel_path)
            if df is None:
                return

            # Tạo biểu đồ
            fig = self.create_sunburst_chart(df)
            if fig is None:
                return

            # Lưu biểu đồ tạm thời và mở trong trình duyệt
            temp_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_curriculum_sunburst.html")
            fig.write_html(
                temp_html_path,
                include_plotlyjs=True,
                full_html=True,
                config={'displayModeBar': True, 'responsive': True}
            )

            # Mở trong trình duyệt
            webbrowser.open('file://' + os.path.realpath(temp_html_path))

            QMessageBox.information(self, "Success", "Chart opened in browser successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error opening chart in browser: {str(e)}")

    def save_chart_to_html(self):
        """Lưu biểu đồ thành file HTML"""
        if not self.excel_path:
            QMessageBox.warning(self, "Warning", "Please select an Excel file first.")
            return

        try:
            # Tạo dữ liệu
            df = self.create_curriculum_data(self.excel_path)
            if df is None:
                return

            # Tạo biểu đồ
            fig = self.create_sunburst_chart(df)
            if fig is None:
                return

            # Mở hộp thoại lưu file
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save HTML File", "411_10k.html", "HTML Files (*.html)"
            )

            if file_path:
                # Lưu biểu đồ thành file HTML
                fig.write_html(
                    file_path,
                    include_plotlyjs=True,
                    full_html=True,
                    config={'displayModeBar': True, 'responsive': True}
                )

                QMessageBox.information(self, "Success", f"Chart saved to {file_path} successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving chart to HTML: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = CurriculumVisualizer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()