// Constantes globales
const N_OCTAVES = 5;
const N_NOTES = 7*N_OCTAVES;
const NOTE_TIME_ON_SCREEN = 5;
const PIANO_TOP_Y_POSITION = 0.7;

//colors
let background_color = '#171717';
let note_color = '#fff';
let colliding_note_color = '#84d7f5';
let shadow_note_color = '#5BBED1';

let piano, noteManager;

class CanvasManager {
    setupCanvas() {
        createCanvas(windowWidth, windowHeight);
    }

    resizeCanvas() {
        resizeCanvas(windowWidth, windowHeight);
    }
}

class Piano {
    constructor(numKeys, keyWidth, keyHeight) {
        this.numKeys = numKeys;
        this.keyWidth = keyWidth;
        this.keyHeight = keyHeight;
    }

    draw(REFERENCE_LINE_Y_POSITION) {
        drawingContext.shadowOffsetY = 3;
        drawingContext.shadowBlur = 3;
        drawingContext.shadowColor = 'rgba(0,0,0,0.25)';
        for (let i = 0; i < this.numKeys; i++) {
            const x = i * this.keyWidth;
            fill(240);
            rect(x, REFERENCE_LINE_Y_POSITION, this.keyWidth, this.keyHeight,3); // Tecla blanca
            stroke(0);
            line(x + this.keyWidth, REFERENCE_LINE_Y_POSITION, x + this.keyWidth, height);
        }

        for (let i = 1; i < this.numKeys; i++) {
            const x = i * this.keyWidth;
            const isWhiteKey = i % 7 === 0 || i % 7 === 3;

            if (!isWhiteKey) {
                fill(0);
                rect(x - this.keyWidth / 4, REFERENCE_LINE_Y_POSITION, this.keyWidth / 2, this.keyHeight * 0.6,3); // Tecla negra
            }
        }
        drawingContext.shadowOffsetY = 0;
        drawingContext.shadowBlur = 0;
        this.drawGradientRect(REFERENCE_LINE_Y_POSITION, height, 90);
    }

    drawGradientRect(yPosition, rectHeight, angleDegrees) {
      // Define la posición y el tamaño del rectángulo con gradiente
        noStroke();
      let x = 0;
      let y = yPosition - rectHeight;
      let w = width; // El ancho del rectángulo es igual al ancho de la pantalla
      let h = rectHeight; // Altura del rectángulo

      // Calcular los puntos finales del gradiente basados en el ángulo
      let angleRadians = radians(angleDegrees);
      let xEnd = x + cos(angleRadians) * w;
      let yEnd = y + sin(angleRadians) * h;

      // Crea un gradiente lineal usando el contexto de dibujo
      let gradient = drawingContext.createLinearGradient(x, y, xEnd, yEnd);

      // Define los colores del gradiente
      gradient.addColorStop(0, 'rgba(91,190,209,0)'); // Inicio del gradiente
      gradient.addColorStop(1, 'rgba(91,190,209,0.2)'); // Final del gradiente

      // Aplica el gradiente y dibuja el rectángulo
      drawingContext.fillStyle = gradient;
      rect(x, y, w, h);
    }


}

class Note {
    constructor(start_time, end_time, frequency) {
        this.start_time = start_time;
        this.end_time = end_time;
        this.frequency = frequency;
    }

    get duration() {
        return this.end_time - this.start_time;
    }

    get height() {
        return (this.duration / NOTE_TIME_ON_SCREEN) * height;
    }

    get xPosition() {
        return ((this.frequency+0.25) / N_NOTES) * width;
    }

    yPosition(time_passed) {
        return (((-this.start_time+time_passed/1000) / NOTE_TIME_ON_SCREEN) * height);
    }

    isColliding(time_passed, REFERENCE_LINE_Y_POSITION){
        return this.yPosition(time_passed) + this.height >= REFERENCE_LINE_Y_POSITION;
    }

    isDead(time_passed, REFERENCE_LINE_Y_POSITION){
        return this.yPosition(time_passed) >= REFERENCE_LINE_Y_POSITION;
    }

    draw(time_passed, REFERENCE_LINE_Y_POSITION){
        drawingContext.shadowBlur = 6;
        drawingContext.shadowColor = '#5BBED1';
        if (this.isDead(time_passed, REFERENCE_LINE_Y_POSITION)){
            console.log("SAMORIO");
        }
        else if (this.isColliding(time_passed, REFERENCE_LINE_Y_POSITION)){
            drawingContext.shadowBlur = 10;
            fill(colliding_note_color);
        }
        else{
            fill(note_color);
        }

        noStroke();
        rect(this.xPosition, this.yPosition(time_passed), 0.5*width / N_NOTES, this.height, 7);
        drawingContext.shadowBlur = 0;
    }
}

class NoteManager {
    constructor() {
        this.REFERENCE_LINE_Y_POSITION = PIANO_TOP_Y_POSITION*height;
        this.notes = [];
        this.start_time = performance.now();
    }

    addNote(start_time, end_time, frequency) {
        this.notes.push(new Note(start_time, end_time, frequency));
    }

    drawNotes() {
        console.log(this.notes.length);
        const time_passed = performance.now() - this.start_time;

        for (let i = this.notes.length - 1; i >= 0; i--) {
            const note = this.notes[i];
            note.draw(time_passed, this.REFERENCE_LINE_Y_POSITION);

            if (note.isDead(time_passed, this.REFERENCE_LINE_Y_POSITION)) {
                this.notes.splice(i, 1); // Elimina el elemento en la posición i
            }
        }
    }

}

const canvasManager = new CanvasManager();

function setup() {
    canvasManager.setupCanvas();
    noteManager = new NoteManager();

    const keyWidth = windowWidth / N_NOTES;
    const keyHeight = height-noteManager.REFERENCE_LINE_Y_POSITION;
    piano = new Piano(N_NOTES, keyWidth, keyHeight);

    // Ejemplo de cómo agregar notas
    noteManager.addNote(0, 1, 5);
    noteManager.addNote(0, 1, 10);
    noteManager.addNote(0, 2, 8);
    noteManager.addNote(3, 4, 6);

}

function draw() {
    background(background_color);
    noteManager.drawNotes();
    piano.draw(noteManager.REFERENCE_LINE_Y_POSITION);
}

function windowResized() {
    canvasManager.resizeCanvas();
}
