# Nand2Tetris — Part 1: Hardware

This repository contains my completed projects for **Part 1** of the *Nand2Tetris* course. The work is organized into 6 modules, each representing a major step in building a functional 16-bit computer from the ground up with a dedicated assembler, I have designed every component using Logisim, an open source software used to design and simulate logic circuits, therefore able to run the Hack computer and make it execute the code live !

Each module includes:

* **HDL implementations** (`HDL/`) of the chips or components.
* **Logisim simulations** (`circ/`) to visualize and test the hardware.
* **(Assembler only)**: A complete **Python assembler** implementation (last module).

Below is an overview of each module with a description and an attached picture of the circuit.

---

## 📘 Module 1 — Boolean Logic

This module implements the fundamental logic gates used throughout the entire Nand2Tetris computer.

**Contents:**

* Basic gates: `And`, `Or`, `Not`, `Xor`, `Mux`, `DMux`, `Not16`, `And16`, `Or16`, `Mux16`, `Or8Way`, `Mux4Way16`, `Mux8Way16`, `DMux4Way`, `DMux8Way`

**Circuit Preview:**
![Boolean Logic Circuits](Pictures/Basic_Gates.png)

---

## 🧮 Module 2 — Boolean Arithmetic

Implements arithmetic primitives such as adders and ALU components.

**Contents:**

* Half Adder, Full Adder, 16-bit Adder
* Incrementer
* ALU implementation

**Circuit Preview:**
* ALU
![ALU Circuit](Pictures/ALU.png)

---

## 🧠 Module 3 — Memory

Implements all memory-related hardware, including the RAM modules.

**Contents:**

* Bit, Register
* RAM8, RAM64, RAM512, RAM4K, RAM16K
* Program Counter

**Circuit Preview:**
* RAM
![RAM Circuit](Pictures/8RAM.png)

---

## 💾 Module 4 — Machine Language

Implements the Hack machine language execution model.

**Contents:**

Two assembly programs:
* Fill.asm: a program that probs the keyboard and when a key is pressed it fills the screen.
* Multi.asm: performs multiplication between two values stored in memory addresses R1 and R2.

## 🖥️ Module 5 — Computer Architecture

Builds the complete Hack CPU and integrates it with memory to create a full 16-bit computer, with a 32 x 32 screen and a keyboard attached.

**Contents:**

* ALU integration
* CPU implementation
* Complete computer (CPU + Memory + ROM)

**Circuit Preview:**
* CPU
![CPU Circuit](Pictures/CPU.png)
* Computer
![Computer Architecture Circuit](Pictures/Computer.png)

---

## 🧩 Module 6 — Assembler

A full assembler written in Python that translates Hack assembly (`.asm`) into a hex machine code (`.bin`) that can be loaded directly into the logisim computer ROM.

**Contents:**

* Assembler

---

## 📄 License

This project is open-source and available under the MIT License.
