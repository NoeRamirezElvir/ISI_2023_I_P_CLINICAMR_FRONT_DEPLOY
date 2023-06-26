//corregir json
function corregirDatosHidden() {
    var datosHidden = document.getElementById("datosHidden").value;
    var datosCorregidos = datosHidden.replace(/'/g, '"').replace(/None/g, 'null').replace(/\\/g, '\\\\');
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

    if (datosHidden.trim() === '[]') {
        alert('No se puede exportar, los datos están vacíos');
        return; // Salir de la función sin realizar más procedimientos
    }

    var datosManipulados = listaDatos.map(function(dato) {
        return {
        ID: dato.id,
        Medicamento: dato.idmedicamento.nombre,
        Precio: dato.precio,
        FechaInicio: dato.fechaInicio,
        FechaFinal: dato.fechaFinal
        };
});

var workbook = XLSX.utils.book_new();

var worksheet = XLSX.utils.json_to_sheet(datosManipulados, { origin: "A4" });
XLSX.utils.book_append_sheet(workbook, worksheet, "Datos");

var fecha = new Date().toLocaleDateString();
var hora = new Date().toLocaleTimeString();
var encabezados = [
    ["Reporte de Precio Historico Medicamento"],
    ["Usuario: " + datosHiddenUsuario, "Fecha: " + fecha, "Hora: "+ hora]
];
XLSX.utils.sheet_add_aoa(worksheet, encabezados, { origin: "A1" });

var fechaActual = new Date().toLocaleDateString();
var nombreArchivo = "datos_" + fechaActual + ".xlsx";
XLSX.writeFile(workbook, nombreArchivo);
});


document.getElementById("exportBtn").addEventListener("click", function() {
var datosHidden = document.getElementById("datosHidden").value;
var datosHiddenUsuario = document.getElementById("datosHiddenUsuario").value;
if (datosHidden.trim() === '[]') {
    alert('No se puede exportar, los datos están vacíos');
    return; // Salir de la función sin realizar más procedimientos
}


var datos = JSON.parse(datosHidden);

var fecha = new Date().toLocaleDateString();
var hora = new Date().toLocaleTimeString();

var docDefinition = {
    content: [
    {
        canvas: [
            {
                type: 'rect',
                x: 0,
                y: 0,
                w: 90,
                h: 50,
                color: '#23574B'
            }
        ]
    },
    {
        absolutePosition: { x: 50, y: 50 },
        stack: [
            {
                width: '100%',
                image: 'logo',
                fit: [65, 45],
                alignment: 'left'
            }
        ],
        margin: [0, 0, 0, 10]
    },
    { text: 'Reporte de Precio Historico Medicamento', style: 'header', alignment: 'center' },
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
        widths: [15, 150, 100, 105,105],
        body: [
            [
            { text: 'ID', style: 'tableHeader', fillColor: '#C6C6C6' },
            { text: 'Medicamento', style: 'tableHeader', fillColor: '#C6C6C6' },
            { text: 'Precio', style: 'tableHeader', fillColor: '#C6C6C6' },
            { text: 'Fecha Inicio', style: 'tableHeader', fillColor: '#C6C6C6' },
            { text: 'Fecha Final', style: 'tableHeader', fillColor: '#C6C6C6' }
            ],
            ...datos.map(function(dato, index) {
            return [
                { text: dato.id, fillColor: index % 2 === 0 ? '#E5E5E5' : '#D9D9D9',style:'name' },
                { text: dato.idmedicamento.nombre, fillColor: index % 2 === 0 ? '#E5E5E5' : '#D9D9D9',style:'name' },
                { text: dato.precio, fillColor: index % 2 === 0 ? '#E5E5E5' : '#D9D9D9',style:'name' },
                { text: dato.fechaInicio, fillColor: index % 2 === 0 ? '#E5E5E5' : '#D9D9D9',style:'name' },
                { text: dato.fechFinal, fillColor: index % 2 === 0 ? '#E5E5E5' : '#D9D9D9',style:'name' }
            ];
            })
        ]
        }
    }
    ],
    images: {
    logo: window.varImagen
    },
    styles: {
    header: {
        fontSize: 18,
        bold: true
    },
    name: {
        fontSize: 10,
        bold: false
    },
    tableHeader: {
        bold: true,
        fillColor: '#CCCCCC'
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
        stack: [
        { canvas: [{ type: 'line', x1: 50, y1: 10, x2: 550, y2: 10 }] },
        { text: 'Página ' + currentPage.toString() + ' de ' + pageCount.toString(), style: 'footer' }
        ]
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