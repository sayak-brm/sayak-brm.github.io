---
draft: true
gallery: []
project_status: "Ongoing"
summary: "I built a BadUSB device with an ESP8266 and an Arduino Pro Micro which can be accessed and controlled via WiFi."
title: "WiFiDucky"
[dates]
completed_on: ""
started_on: "2019-01-03T00:00:00+05:30"
---

Around four months back I started reading about and experimenting with RubberDuckies and the BadUSB attack vector, which basically consisted of a microcontroller plugged into a computer emulating input devices like mice and keyboards. Such a device could essentially get full control of the host computer, essentially bypassing all software security measures like anti-viruses and firewalls.

## BadUSB

Imagine you could walk up to a computer, plug in a seemingly innocent USB drive, and have it install a backdoor, exfiltrate documents, steal passwords or any number of pentest tasks. All of these things can be done with many well crafted keystrokes. If you could just sit in front of this computer, with photographic memory and perfect typing accuracy, you could do all of these things in just a few minutes.

A BadUSB attack does this in seconds. It violates the inherent trust computers have in humans by posing as an HID devices and injecting keystrokes at superhuman speeds.
