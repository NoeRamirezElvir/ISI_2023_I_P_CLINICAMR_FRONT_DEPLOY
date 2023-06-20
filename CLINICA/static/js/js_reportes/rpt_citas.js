//corregir json
function corregirDatosHidden() {
    var datosHidden = document.getElementById("datosHidden").value;
    var datosCorregidos = datosHidden.replace(/'/g, '"').replace(/\\/g, '\\\\');
    document.getElementById("datosHidden").value = datosCorregidos;
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    corregirDatosHidden();
  });
  
    //excell
  document.getElementById("exportarBtn").addEventListener("click", function() {
    var datosHidden = document.getElementById("datosHidden").value;
    var datosHiddenUsuario = document.getElementById("datosHiddenUsuario").value;
    var listaDatos = JSON.parse(datosHidden);
  
    var datosManipulados = listaDatos.map(function(dato) {
      return {
        ID: dato.id,
        Paciente: dato.idPaciente.nombre + " / " + dato.idPaciente.documento,
        fechaRegistro: dato.fechaActual,
        fechaProgramada: dato.fechaProgramada,
        fechaMaxima: dato.fechaMaxima
      };
    });
  
    var workbook = XLSX.utils.book_new();
  
    var worksheet = XLSX.utils.json_to_sheet(datosManipulados, { origin: "A4" });
    XLSX.utils.book_append_sheet(workbook, worksheet, "Datos");
  
    var fecha = new Date().toLocaleDateString();
    var hora = new Date().toLocaleTimeString();
    var encabezados = [
      ["Reporte de Citas"],
      ["Usuario: " + datosHiddenUsuario, "Fecha: " + fecha, "Hora: "+ hora]
    ];
    XLSX.utils.sheet_add_aoa(worksheet, encabezados, { origin: "A1" });

    var fechaActual = new Date().toLocaleDateString();
    var nombreArchivo = "datos_" + fechaActual + ".xlsx";
    XLSX.writeFile(workbook, nombreArchivo);
  });
  
  //pdf
  document.getElementById("exportBtn").addEventListener("click", function() {
    var datosHidden = document.getElementById("datosHidden").value;
    var datosHiddenUsuario = document.getElementById("datosHiddenUsuario").value;
    var datos = JSON.parse(datosHidden);
  
    var fecha = new Date().toLocaleDateString();
    var hora = new Date().toLocaleTimeString();

    var docDefinition = {
      content: [
        { text: 'Reporte de Citas', style: 'header', alignment: 'center' },
        { text: '\n' },
        { text: 'Fecha: ' + fecha + ' ' + hora, style: 'name' },
        { text: '\n' },
        { text: 'Usuario: ' + datosHiddenUsuario, style: 'name' },
        { text: '\n' },
        { canvas: [{ type: 'line', x1: 0, y1: 10, x2: 520, y2: 10 }] },
        { text: '\n' },
        {
          table: {
            headerRows: 1,
            widths: [15,115,115,115,115], // Anchura de las columnas
            body: [
              ['ID', 'Paciente/Documento', 'Fecha de Registro','Fecha Programada', 'Fecha Maxima'], // Encabezado
              ...datos.map(function(dato) {
                return [
                  dato.id,
                  dato.idPaciente.nombre + " / " + dato.idPaciente.documento,
                  dato.fechaActual,
                  dato.fechaProgramada,
                  dato.fechaMaxima
                ];
              })
            ]
          }
        }
      ],
      styles: {
        header: {
          fontSize: 18,
          bold: true
        },
        name: {
          fontSize: 12,
          bold: true
        },
        line: {
          margin: [0, 5, 0, 5]
        },
        footer: {
          fontSize: 10,
          alignment: 'right',
          margin: [0, 10, 40, 0]
        }
      },
      footer: function(currentPage, pageCount) {
        return {
          text: 'Página ' + currentPage.toString() + ' de ' + pageCount.toString(),
          style: 'footer'
        };
      },
      
      afterPageContent: function(data) {
        docDefinition.footer = function(currentPage, pageCount) {
          return {
            text: 'Página ' + currentPage.toString() + ' de ' + pageCount.toString(),
            style: 'footer'
          };
        };
      }
    };
  
    pdfMake.createPdf(docDefinition).download("datos.pdf");
  });
  