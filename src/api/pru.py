@csrf_exempt
def downloadDuplicados(request):
    if request.method == 'GET':

        workbook = opxl.load_workbook('tmp/rec.xlsm', read_only=False, keep_vba=True)
        worksheet = workbook.active

        fechaR = datetime.datetime.today().strftime('%d-%m-%y')
        
        # duplicados = RescatePunto.objects.all()

        register3 = RescatePunto.objects.values("iso3", "nombre", "apellidos", "fechaNacimiento").annotate(records=Count("*")).filter(records__gt=1)
        duplicados = []
        for reg in register3:
            for registro in RescatePunto.objects.filter(iso3=reg['iso3'], nombre=reg['nombre'], apellidos = reg['apellidos'], fechaNacimiento=reg['fechaNacimiento']):
                duplicados.append(registro)
                
        for valor in duplicados:
            puntoR = ""
            if valor.aeropuerto:
                puntoR = 'aeropuerto'
            elif valor.carretero:
                puntoR = 'carretero'
            elif valor.centralAutobus:
                puntoR = 'central de autobus'
            elif valor.casaSeguridad:
                puntoR = 'casa de seguridad'
            elif valor.ferrocarril:
                puntoR = 'ferrocarril'
            elif valor.hotel:
                puntoR = 'hotel'
            elif valor.puestosADispo:
                puntoR = 'puestos a disposicion'
            elif valor.voluntarios:
                puntoR = 'voluntarios'
            else: 
                puntoR = ''
            worksheet.append([valor.oficinaRepre, 
                              valor.fecha,
                              valor.hora,
                              valor.nombreAgente.upper(),
                              puntoR.upper(),
                              valor.puntoEstra.upper(),
                              valor.nacionalidad.upper(),
                              valor.iso3,
                              valor.nombre.upper(),
                              valor.apellidos.upper(),
                              valor.noIdentidad,
                              valor.parentesco.upper(),
                              valor.fechaNacimiento,
                              "Hombre" if valor.sexo else "Mujer",
                              "1" if valor.embarazo else "",
                              valor.numFamilia if valor.numFamilia != 0 else "",
                              valor.edad,
                              ])

        response = HttpResponse(content = save_virtual_workbook(workbook), content_type='application/vnd.ms-excel.sheet.macroEnabled.12')
        response['Content-Disposition'] = 'attachment; filename={fecha}.xlsm'.format(fecha = fechaR)

        return response