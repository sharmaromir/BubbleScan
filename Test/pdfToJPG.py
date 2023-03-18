from pdf2image import convert_from_path

def convertToImg(pdf_path, directory):
    pdfs = pdf_path
    print(pdfs)
    pages = convert_from_path(pdfs, 100, poppler_path='poppler-23.01.0/Library/bin')

    i = 0
    for page in pages:
        image_name = "Page_" + str(i) + ".jpg"  
        page.save(directory +"/" + image_name, "JPEG")
        i = i+1    
    return(len(pages)) 