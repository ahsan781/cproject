$(document).ready(function() {
    $('#Skill_type')[0].addEventListener('change', (event) => {
        let sequelField = $('#skill').parents('p');
        if (event.target.checked) {
            sequelField.show();
        } else {
            sequelField.hide();
        }
    })
});