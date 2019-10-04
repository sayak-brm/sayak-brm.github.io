---
title: "Designing a C Compiler, Part 1"
date: 2019-08-01T18:02:29+05:30
draft: true
toc: false
images:
tags:
  - python
  - c
  - compilers
  - compiler-design
---

This is the first entry in a series on writing a C compiler called `nacc` (Not Another C Compiler) in Python as a learning experiment. Some reasons I decided to take up this project:

 1. To learn about the gritty, low-level functioning of computers and assembly language, and the working of compilers.
 1. To feel like an a badass because for several this seems like an impossibly difficult project.

## Compiler Structure

I'm using Abdulaziz Ghuloum’s paper on [An Incremental Approach to Compiler Construction](http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf) and [Nora Sandler](https://norasandler.com/)'s [nqcc](https://github.com/nlsandler/nqcc) as roadmap for this project and decided to implement it in Python due to its flexiblity. The compiler will target Intel x86 assembly, which will then be assembled and executed via the [PyCCA](https://github.com/pycca/pycca) Assembler library.

The compiler I'm writing will be a fairly standard compiler architecture and will be divided into three primary parts: a lexer, a parser, and a code generator.

## The Lexer

The lexer, also called lexical analyzer or tokenizer, is a program that breaks down the input source code into a sequence of tokens. It reads the input source code character by character, recognizes and labels the tokens and outputs them sequentially. I've used the excellent collection of tools from the [partpy](https://pypi.org/project/partpy/) library to speed up the development of the lexer of `nacc`.
