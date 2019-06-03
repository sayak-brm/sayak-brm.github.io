---
title: "WiFiDucky"
date: 2019-06-03T13:11:58+05:30
summary: I built a BadUSB device with an ESP12 and an Arduino Pro Micro which can be accessed and controlled via WiFi.
draft: true
---

Around four months back I started reading about and experimenting with RubberDuckies and the BadUSB attack vector, which basically consisted of a microcontroller plugged into a computer emulating input devices like mice and keyboards. Such a device could essentially get full control of the host computer, essentially bypassing all software security measures like anti-viruses and firewalls.

## BadUSB

Imagine you could walk up to a computer, plug in a seemingly innocent USB drive, and have it install a backdoor, exfiltrate documents, steal passwords or any number of pentest tasks. All of these things can be done with many well crafted keystrokes. If you could just sit in front of this computer, with photographic memory and perfect typing accuracy, you could do all of these things in just a few minutes.

A BadUSB attack does this in seconds. It violates the inherent trust computers have in humans by posing as an HID devices and injecting keystrokes at superhuman speeds.
