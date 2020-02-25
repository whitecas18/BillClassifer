# Author: Dillon Roberts
# E-mail: robertsd13@students.ecu.edu
# CLA: DIR_PATH* FILE_PATH OUT_PATH
# Requirements: 
# 	PDFs must be <=1.7
#		Only English characters expected
# Desc: Given path to a directory of pdfs, or file, output the files as text
# with UTF-8 formatting.

import PyPDF2
import pathlib

class pdf2txt:
	def __init__(self, f_path=pathlib.Path, d_path=[], out_path=pathlib.Path, verbosity=0):
		self.d_path = d_path
		self.f_path = f_path
		self.out_path = out_path
		self.verbosity = verbosity
		if(verbosity>0):
			self.log_paths()

	def log_paths(self):
		# Log all the current paths
		print("Current Paths:")
		for path in self.d_path:
			print("\tDir - ",path)
		for path in self.f_path:
			print("\tFile - ", path)
		print("\tOutputting to ",self.out_path)
		
	def process_files(self):
		file = pathlib.Path
		for file in self.f_path:
			pdfFile = open(file, 'rb')
			txtFilePath = self.out_path.joinpath(file.name[:-3])
			outFile = open(txtFilePath, "a+")
			if self.verbosity >= 2:
				print(txtFilePath)

			pdfReader = PyPDF2.PdfFileReader(pdfFile)
			numPages = pdfReader.getNumPages()
			for pageNum in range(0,numPages):
				page = pdfReader.getPage(pageNum)
				outFile.write(page.extractText())
				if self.verbosity >= 2:
					outFile.write('---PAGE ' + str(pageNum) + '---')

			outFile.close()
			pdfFile.close()

testPath = pathlib.Path(r"D:/School/CSCI4140/Project/files/b/data/test_docs/test_CREC-2020-02-21.pdf")
testOut = testPath.parent
tester = pdf2txt([testPath],out_path=testOut,verbosity=2)
tester.process_files()
