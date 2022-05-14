const loaderAlert = () => {
    Swal.fire({
        title: "Por favor, espere estamos clasificando los resultados, esto puede tardar algúnos minutos",
        html: "Cargando información necesaria...",
        allowOutsideClick: !1,
        showConfirmButton: false,
        timer: 3000,
        willOpen: () => {
            Swal.showLoading();
        },
    }).then(function() {
        $("#resultados").css("display", "block");

    });
};

const explicacionResultados = () => {
    Swal.fire({
        title: "",
        width: 2000,
        html: `      <table class="table text-black">
    <thead>
      <tr>
        <th>Categoría 1</th>
        <th>Categoría 2</th>
        <th>Categoría 3</th>
        <th>Categoría 4</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>"Estereotipo: define aquellos mensajes cuyo contenido hace referencia a un
estereotipo u objetificación. Son mensajes que hablan de una imagen o una
idea generalizada y simplificada de la mujer. Suelen estar relacionados con
aspectos referentes al físico y tienden a realizar comparaciones con estándares impuestos."</td>  
        <td>Desvío de atención: definen mensajes que tienden a desviar la atención de un problema y con el fin de justificar el abuso   se rechaza la responsabilidad masculina. Es una forma de interrumpir la conversación y redirigirla a un ámbito más cómodo para los hombres</td>  
        <td>Ataque sexual: hace referencia a mensajes en los que está presente acciones de acoso sexual o amenazas violentas con el fin de afirmar el poder</td>  
        <td>Descrédito/desprestigio: hace referencia a casos de desprestigio hacia una mujer. El fin de
estos tweets es hablar mal de una mujer sin ningún otro objetivo.</td>  
      </tr>
    </tbody>
  </table>`,
    });
};

$("#addTextButton").click(function() {
    const html = `<div class="mb-3"><textarea name="text[]" class="cnt form-control" cols="30" rows="1"></textarea></div>`;
    $("#textos").append(html);
});

$("#saveBtn").click(function() {
    const arr = [];
    $(".cnt").each(function() {
        arr.push($(this).val());
    });
    loaderAlert();
    $("#resultados").css("display", "none");
    $.ajax({
        url: '/checkMessage',
        type: "post",
        data: {
            textos: arr
        },
        success: function(res) {
            const respuesta = JSON.parse(res);
            console.log(respuesta);
            fillTable(respuesta, arr);
            Swal.close();
        },
    });
});

const fillTable = (respuesta, textos) => {
    let html = ``;

    textos.forEach((txt, index) => {
        html += `<tr>
      <td>${txt}</td>
      <td>${respuesta.label[index] ? "Afirmativo" : "Negativo"}</td>
      <td>${respuesta.category1[index] ? "Afirmativo" : "Negativo"}</td>
      <td>${respuesta.category2[index] ? "Afirmativo" : "Negativo"}</td>
      <td>${respuesta.category3[index] ? "Afirmativo" : "Negativo"}</td>
      <td>${respuesta.category4[index] ? "Afirmativo" : "Negativo"}</td>
      <td>${respuesta.single[index] ? "Afirmativo" : "Negativo"}</td>
      <td>${respuesta.groups[index] ? "Afirmativo" : "Negativo"}</td>
    </tr>`;
    });
    $("#bodyTable").html("");
    $("#bodyTable").append(html);
    $("#resultados").css("display", "block");

    const reload = `<div class="mb-3"><textarea name="text[]" class="cnt form-control" cols="30" rows="1"></textarea></div>`;
    $("#textos").html(reload);
};
const disclaimer = () => {
    Swal.fire(
        "Los resultados de la inteligencia artificial están basados en el análisis matemáticos de un conjunto de textos establecidos como misóginos o no misóginos, el resultado puede fallar o discordar de la realidad si este contiene palabras establecidas como clave en un contexto no clasificado como misógino. Esta aplicación está en desarrollo y los resultados no deben tomarse como una clasificación oficial, Se recomienda la búsqueda de ayuda profesional en caso sea necesario "
    );
};