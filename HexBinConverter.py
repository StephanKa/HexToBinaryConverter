import time
import binascii
from PyQt4 import QtGui, QtCore
import sys

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Hex-Binary-Converter')
        # set the layout
        self.setFixedSize(800, 600)
        self.main_widget = QtGui.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.total_bits = 32
        self.highlight_bit = [1]
        self.number_bits_in_row = 1
        
        font = QtGui.QFont()
        font.setBold(True)
        
        self.layout_hex_field = QtGui.QVBoxLayout()
        self.layout_binary_field = QtGui.QVBoxLayout()
        self.text_edit_field_convert = QtGui.QTextEdit()
        
        bit_highlight_hbox = QtGui.QHBoxLayout()
        highlight_label = QtGui.QLabel()
        highlight_label.setFont(font)
        highlight_label.setText('Highlight Bit: ')
        self.text_edit_bit_highlight = QtGui.QTextEdit()
        self.text_edit_bit_highlight.setFixedSize(300, 25)
        self.text_edit_bit_highlight.setText(str(self.highlight_bit).replace('[', '').replace(']', '').replace(',', ''))
        bit_highlight_hbox.addWidget(highlight_label)
        bit_highlight_hbox.addWidget(self.text_edit_bit_highlight)
        
        number_bits_highlight_hbox = QtGui.QHBoxLayout()
        number_of_bits_label = QtGui.QLabel()
        number_of_bits_label.setFont(font)
        number_of_bits_label.setText('Number of Bits in row: ')
        self.text_edit_bit_number = QtGui.QTextEdit()
        self.text_edit_bit_number.setFixedSize(300, 25)
        self.text_edit_bit_number.setText(str(self.number_bits_in_row))
        number_bits_highlight_hbox.addWidget(number_of_bits_label)
        number_bits_highlight_hbox.addWidget(self.text_edit_bit_number)
        
        total_bit_hbox = QtGui.QHBoxLayout()
        total_bit_label = QtGui.QLabel()
        total_bit_label.setText('Total Bits: ')
        total_bit_label.setFont(font)
        self.text_edit_total_bits = QtGui.QTextEdit()
        self.text_edit_total_bits.setFixedSize(300, 25)
        self.text_edit_total_bits.setText(str(self.total_bits))
        total_bit_hbox.addWidget(total_bit_label)
        total_bit_hbox.addWidget(self.text_edit_total_bits)
        
        self.text_edit_field_converted = QtGui.QTextEdit()
        self.text_edit_field_converted.setReadOnly(True)
        
        self.convert_button = QtGui.QPushButton('Convert')
        self.convert_button.clicked.connect(self._convert)
        
        convert_hex = QtGui.QLabel()
        convert_hex.setFont(font)
        convert_hex.setText('List of Hex-Strings:')
        
        converted_binary = QtGui.QLabel()
        converted_binary.setFont(font)
        converted_binary.setText('List of converted strings:')
        
        self.layout_hex_field.addLayout(total_bit_hbox)
        self.layout_hex_field.addLayout(bit_highlight_hbox)
        self.layout_hex_field.addLayout(number_bits_highlight_hbox)
        
        self.layout_hex_field.addWidget(convert_hex)
        self.layout_hex_field.addWidget(self.text_edit_field_convert)
        self.layout_hex_field.addWidget(self.convert_button)
        self.layout_binary_field.addWidget(converted_binary)
        self.layout_binary_field.addWidget(self.text_edit_field_converted)
        
        hbox = QtGui.QHBoxLayout(self.main_widget)
        hbox.addLayout(self.layout_hex_field)
        hbox.addLayout(self.layout_binary_field)
        self.setLayout(hbox)
    
    def _convert(self):
        hex_string = str(self.text_edit_field_convert.toPlainText())
        temp_hex_list = hex_string.replace('\r', '').split('\n')
        self.total_bits = int(str(self.text_edit_total_bits.toPlainText()), 10)
        binary_string = ''
        index = 1
        hex_string = ''
        for temp_bin in temp_hex_list:
            if(temp_bin == ''):
                continue
            if('\t' in temp_bin):
                temp_bin = temp_bin[temp_bin.find('\t') + 1:]
            binary_string += '{0}.\t'.format(index)
            hex_string += '{0}.\t'.format(index)
            binary = bin(int(temp_bin, 16))[2:]
            if(len(binary) > self.total_bits):
                self.total_bits = len(binary)
                self.text_edit_total_bits.setText(str(self.total_bits))
            binary_string += bin(int(temp_bin, 16))[2:].zfill(self.total_bits) + '\n'
            hex_string += temp_bin + '\n'
            index += 1
        self.text_edit_field_convert.clear()
        self.text_edit_field_converted.clear()
        self.text_edit_field_convert.setText(hex_string)
        self.text_edit_field_converted.setText(binary_string)
        self._highlight()
        
    def _highlight(self):
        cursor = self.text_edit_field_converted.textCursor()
        number_of_bits = int(str(self.text_edit_bit_number.toPlainText()), 10)
        hex_string = str(self.text_edit_field_converted.toPlainText())
        temp_string = hex_string.split('\n')
        format = QtGui.QTextCharFormat()
        len_carriage_return = 1
        len_bit_offset = 1
        bits_for_highlight = str(self.text_edit_bit_highlight.toPlainText()).replace('[', '').replace(']', '').replace(',', '').split(' ')
        self.highlight_bit = [int(temp, 10) for temp in bits_for_highlight] 
        len_string = 0
        for temp in temp_string:
            if(temp == ''):
                break
            len_string += len(temp)
            for i in range(number_of_bits):
                for temp_bits in self.highlight_bit:
                    if((temp[len(temp) - len_bit_offset - temp_bits + i: len(temp) - len_bit_offset - temp_bits + 1 + i]) == '1'):
                        format.setBackground(QtGui.QBrush(QtGui.QColor("green")))
                    else:
                        format.setBackground(QtGui.QBrush(QtGui.QColor("red")))
                    cursor.setPosition(len_string - len_bit_offset - temp_bits + i)
                    cursor.movePosition(QtGui.QTextCursor.Right, 1)
                    cursor.mergeCharFormat(format)
            len_string += len_carriage_return
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())