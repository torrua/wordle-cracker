const numbersOfIterations = 5
const numberOfChars = 5

const colorBlack = '#989898'
const colorYellow = '#C6B566'
const colorGreen = '#79A86B'
const colorWhite = '#FFFFFF'

function generateEmptyTable() {

    const board = document.querySelector('#board')

    for (r = 1; r < numbersOfIterations + 1; r++) {
        const iteration = document.createElement('div')
        iteration.classList.add('iteration')

        for (c = 1; c < numberOfChars + 1; c++) {
            var char = document.createElement('div')
            char.classList.add('char')

            if (r === 1 && c === 1) {
                char.classList.add('current')
                iteration.classList.add('current')
            }

            char.setAttribute("status", colorWhite)
            char.addEventListener('click', charClicked)

            iteration.append(char)
        }
        board.append(iteration)
    }
}

function generateKeyboard() {

    const keyboardRow1 = ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ']
    const keyboardRow2 = ['Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э']
    const keyboardRow3 = ['⌫', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', '⏎']
    const keyboard = [keyboardRow1, keyboardRow2, keyboardRow3]
    const kb = document.querySelector('#kb')

    for (let rowIndex in keyboard) {

        const row = document.createElement("div")
        row.classList.add('row')
        const rowData = keyboard[rowIndex]

        for (let keyIndex in rowData) {
            const key = document.createElement("button")
            key.setAttribute("id", rowData[keyIndex])
            addKeyEventListeners(key, rowData[keyIndex])
            addKeyClasses(key, rowData[keyIndex])
            key.innerHTML = rowData[keyIndex]
            row.append(key)
        }

        kb.append(row)
    }
}

function addKeyClasses(key, value) {

    key.classList.add('key')

    if (value === '⏎') {
        key.classList.add('enter')
    }
    else if (value === '⌫') {
        key.classList.add('backspace')
    }
}


function addKeyEventListeners(key, value) {
    if (value === '⏎') {
        key.addEventListener('click', enterPressed)
    }
    else if (value === '⌫') {
        key.addEventListener('click', backspacePressed)
    }
    else {
        key.addEventListener('click', keyPressed)
    }
}

function keyPressed(event) {
    const value = event.target.firstChild.nodeValue
    fillCurrentChar(value)
    prepareNextChar()
}

function fillCurrentChar(value) {
    const char = document.querySelector(".current.char")
    if (!char) { return }
    char.innerHTML = value
}

function enterPressed(event) {
    console.log('enterPressed')
    clearSuggestions()
    const collectedCharsData = collectData()
    if (Object.keys(collectedCharsData).length === 0) { return }
    sendRequest(collectedCharsData)
}

function backspacePressed(event) {
    console.log('backspacePressed')
    clearSuggestions()

    const filledChars = document.querySelectorAll(".char.filled")
    if (filledChars.length === 0) {
        return
    }
    const currentChar = document.querySelector(".char.current")
    if (currentChar) { currentChar.classList.remove('current') }

    const lastFilledChar = filledChars[filledChars.length - 1]
    lastFilledChar.classList.remove('filled')
    lastFilledChar.classList.add('current')
    lastFilledChar.innerHTML = null

    setColor(lastFilledChar, colorWhite)
}

function convertColorToStatus(colorIndex) {
    switch (colorIndex) {
        case colorBlack:
            return "B"
        case colorYellow:
            return "Y"
        case colorGreen:
            return "G"
        default:
            return "W"
    }
}

function charClicked(event) {
    changeCharStatus(event)
}

function setColor(char, color) {
    char.setAttribute('status', color)
    char.style.backgroundColor = color
    char.style.borderColor = color

    if (color === colorWhite) {
        char.style.borderColor = colorBlack
    }
}

function changeCharStatus(event) {

    const char = event.target
    if (!char.classList.contains('filled')) {
        return
    }

    const status = char.getAttribute("status")
    switch (status) {
        case colorBlack:
            setColor(char, colorYellow)
            break
        case colorYellow:
            setColor(char, colorGreen)
            break
        default:
            setColor(char, colorBlack)
    }
}

function prepareNextChar() {
    const allChars = document.querySelectorAll(".char")
    for (let i = 0; i < numberOfChars * numbersOfIterations; i++) {
        const currentChar = allChars[i]

        if (currentChar.classList.contains('current'))
            {
                markCharAsFilled(currentChar)
                setColor(currentChar, colorBlack)

                if (i < numberOfChars * numbersOfIterations - 1) {
                    const nextChar = allChars[i + 1]
                    markCharAsCurrent(nextChar)
                    break
                }
            }
    }
}

function markCharAsCurrent(char) {
    char.classList.add("current")
}

function markCharAsFilled(char) {
    char.classList.remove('current')
    char.classList.add('filled')
}

function collectData() {
    let allCharsData = {}
    let lowerWord = ''
    let statuses = ''

    const chars = document.querySelectorAll('.char.filled')
    if (chars.length % 5 != 0 || chars.length === 0) {
        return {}
    }

    for (let i = 0; i < chars.length; i++) {
        const currentChar = chars[i]
        lowerWord += currentChar.innerHTML.toLowerCase()
        statuses += convertColorToStatus(currentChar.attributes.status.value)
        if (lowerWord.length === 5) {
            allCharsData[lowerWord] = statuses
            lowerWord = ''
            statuses = ''
        }
    }
    return allCharsData
}

function sendRequest(charsData) {
    let request = new XMLHttpRequest()
    request.addEventListener('load', applyResponse)
    request.open('POST', '/get_suggestions')
    let form_data = new FormData()
		for ( let key in charsData ) { form_data.append(key, charsData[key])}
    request.send(form_data)
}

function applyResponse(event) {
    var data = JSON.parse(event.target.responseText)
    showSuggestions(data)
}

function showSuggestions(data) {
    clearSuggestions()
    const sg = document.querySelector('#sg')
    for (i = 0; i < data.length; i++) {
        const sug = document.createElement("div")
        sug.setAttribute("id", data[i])
        sug.classList.add('suggestion')
        sug.innerHTML = data[i]
        sg.append(sug)
    }
}

function clearSuggestions() {
    const sg = document.querySelector('#sg')
    sg.innerHTML = null
}

generateEmptyTable()
generateKeyboard()