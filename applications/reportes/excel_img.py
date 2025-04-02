import excel2img

def convertir_excel_a_imagen(excel_path, img_path, label, rango):
    return excel2img.export_img(excel_path, img_path, label, rango)