function setup() {
  createCanvas(windowWidth, windowHeight);
  const numKeys = 40; // Número de teclas en el piano
  const keyWidth = windowWidth / numKeys; // Ancho de las teclas
  const keyHeight = keyWidth * 5; // Altura de las teclas

  // Crear el piano
  const piano = new Piano(numKeys, keyWidth, keyHeight);

  // Dibujar el piano
  piano.draw();
}

class Piano {
  constructor(numKeys, keyWidth, keyHeight) {
    this.numKeys = numKeys;
    this.keyWidth = keyWidth;
    this.keyHeight = keyHeight;
  }

  draw() {
    for (let i = 0; i < this.numKeys; i++) {
      const x = i * this.keyWidth;
      fill(255);
      rect(x, 0, this.keyWidth, this.keyHeight); // Tecla blanca
      fill(0);
      line(x + this.keyWidth, 0, x + this.keyWidth, this.keyHeight);
    }


    for (let i = 1; i < this.numKeys; i++) {
      const x = i * this.keyWidth;
      const isWhiteKey = i % 7 === 0 || i % 7 === 3; // Alternar entre teclas negras y blancas

      if (!isWhiteKey) {
        fill(0);
        rect(x-this.keyWidth/4, 0, this.keyWidth/2, this.keyHeight * 0.6); // Tecla negra
      }
    }
  }
}
