/* -------------------------------------------------------------------
    categories
------------------------------------------------------------------- */
function get_categories() {
    fetch('/categories', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + jwt,
            'form': document.forms[0]
        }
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function new_category() {
    fetch('/categories/create', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function new_category_submission() {
    let formData = new FormData(document.forms[0])
    fetch('/categories/create', {
        method: 'POST',
        headers: {'Authorization': 'Bearer ' + jwt},
        body: formData
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        if (myJson['success']) {
            location.reload()
        } else {
            alert('Validation Error!!')
        }
    })
}

function get_category(category_id) {
    fetch('/category/' + category_id, {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function edit_category(category_id) {
    fetch('/category/' + category_id + '/edit', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function edit_category_submission(category_id) {
    let formData = new FormData(document.forms[0])
    fetch('/category/' + category_id + '/edit', {
        method: 'PATCH',
        headers: {'Authorization': 'Bearer ' + jwt},
        body: formData
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        if (myJson['success']) {
            location.reload()
        } else {
            alert('Validation Error!!')
        }
    })
}

function delete_category(category_id) {
    fetch('/category/' + category_id + '/delete', {
        method: 'DELETE',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        location.reload()
    })
}

/* -------------------------------------------------------------------
    types
------------------------------------------------------------------- */
function get_types(category_id) {
    fetch('/types/' + category_id, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + jwt,
            'form': document.forms[0]
        }
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function new_type() {
    fetch('/types/create', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function new_type_submission() {
    let formData = new FormData(document.forms[0])
    fetch('/types/create', {
        method: 'POST',
        headers: {'Authorization': 'Bearer ' + jwt},
        body: formData
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        if (myJson['success']) {
            location.reload()
        } else {
            alert('Validation Error!!')
        }
    })
}

function get_type(type_id) {
    fetch('/type/' + type_id, {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function edit_type(type_id) {
    fetch('/type/' + type_id + '/edit', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function edit_type_submission(type_id) {
    let formData = new FormData(document.forms[0])
    fetch('/type/' + type_id + '/edit', {
        method: 'PATCH',
        headers: {'Authorization': 'Bearer ' + jwt},
        body: formData
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        if (myJson['success']) {
            location.reload()
        } else {
            alert('Validation Error!!')
        }
    })
}

function delete_type(type_id) {
    fetch('/type/' + type_id + '/delete', {
        method: 'DELETE',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        location.reload()
    })
}

/* -------------------------------------------------------------------
    Animals
------------------------------------------------------------------- */
function get_animals(type_id) {
    fetch('/animals/' + type_id, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + jwt,
            'form': document.forms[0]
        }
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function new_animal() {
    fetch('/animals/create', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function new_animal_submission() {
    let formData = new FormData(document.forms[0])
    fetch('/animals/create', {
        method: 'POST',
        headers: {'Authorization': 'Bearer ' + jwt},
        body: formData
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        if (myJson['success']) {
            location.reload()
        } else {
            alert('Validation Error!!')
        }
    })
}

function get_animal(animal_id) {
    fetch('/animal/' + animal_id, {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function edit_animal(animal_id) {
    fetch('/animal/' + animal_id + '/edit', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        document.getElementById('form').innerHTML = myJson['form']
    })
}

function edit_animal_submission(animal_id) {
    let formData = new FormData(document.forms[0])
    fetch('/animal/' + animal_id + '/edit', {
        method: 'PATCH',
        headers: {'Authorization': 'Bearer ' + jwt},
        body: formData
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        if (myJson['success']) {
            location.reload()
        } else {
            alert('Validation Error!!')
        }
    })
}

function delete_animal(animal_id) {
    fetch('/animal/' + animal_id + '/delete', {
        method: 'DELETE',
        headers: {'Authorization': 'Bearer ' + jwt}
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (myJson) {
        location.reload()
    })
}
