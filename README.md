# Edutain

## Problem:

People be watching TikTok/YouTube and not be learning things.

In the age of ***AI*** (aYy-EyE...), it's super easy to fall into the malaise of copy-pasta-ing and not learning.

## Solution:

Edutain.

Shortform lessons about anything the user wants to learn about.

(Note: I'll be workshopping and building this as a CS major. Thinking primarily stats kind of lessons for debugging purposes.)

The user will be quizzed on lesson content, think Duolingo.

The user can come back and review previous lessons, spaced repetition.

## MVP:

Upload an EPUB.

Parse the EPUB and put it in a format that's ingestable for an LLM.

Have the LLM generate a .yml-esque format of flash card questions.

You finish a chapter of your book, head here and complete the flash cards to test comprehension.

Come back later and do some spaced repetition review.

Fin.

## Goal:

You can learn new things and retain the information long-term using this service.

## Tech Stack:

Svelte frontend.

Flask backend.

Firebase/Google Cloud for hosting both.

Firestore for DB.

## Features:

User login/signup flow.

Post-chapter quiz.

Spaced repition review.

Mobile-first UI. iOS "Add to Home Screen" install flow.

## Resources:

https://medium.com/@retzd/exploring-the-power-of-python-with-firebase-cloud-functions-a-comparison-with-microservices-544dcbcb0d51