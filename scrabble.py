import sqlite3 as sql
import tkinter as tk
from tkinter import ttk as tkk
from tkinter import *
import time
import os
import random
import threading
from multiprocessing import Process

try:   
    handle = sql.connect("words.db")
    cursor = handle.cursor()
    cursor.execute("CREATE TABLE WORDS(WORD TEXT, IDLE INT)")
    cursor.execute("CREATE TABLE RESULTS(SCORE TEXT, LENGTH INT, TIME INT)")
    handle.commit()
    handle.close()
except:
    cont = True

class load:

    def __init__(self):
        self.run = True
        self.u = 0
        self.lines = ""

    def loadfiles(self):
        with open('engmix.txt', encoding="latin1") as f:
            self.lines = f.readlines()
        f.close()
        try:
            while self.run == True:
                try:
                    self.lines[self.u] = self.lines[self.u].rstrip()
                    print(self.lines[self.u])
                    handle = sql.connect("words.db")
                    cursor = handle.cursor()
                    cursor.execute("INSERT INTO WORDS VALUES(?,?)", (self.lines[self.u], "0"))
                    handle.commit()
                    handle.close()
                except:
                    self.run = True
                self.u+=1
        except:
            self.run = False
        print("complete")

def close(tab4):
    tab4.destroy()
    
class main:
    
    def __init__(self):
        self.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.vowels = ["a", "e", "i", "o", "u"]
        self.letter = ""
        self.string = ""
        self.length = ""
        self.run = True
        self.run2 = True
        self.user = ""
        self.time = 0
        self.timer = 0
        self.seconds = 0
        self.elapsed = 0
        self.idletrue = True
        self.allinputs = []
        self.tab = ""
        self.score = 0
        self.wordlist = []
        
    def start(self):
        try:
            self.length = int(input("enter a length of string: "))
        except:
            while self.run:
                try:
                    self.length = int(input("enter a length of string: "))
                    self.run = False
                except:
                    self.run = True
        try:
            self.time = int(input("amount of time: "))
        except:
            while self.run2:
                try:
                    self.time = int(input("amount of time: "))
                    self.run2 = False
                except:
                    self.run2 = True
        print(" ")
        print(main.generatestring())
        main.thread()
        
    def generatestring(self):
        for v in range(0, self.length-1):
            self.letter = self.alphabet[random.randint(0, 25)]
            self.string = self.string+" "+str(self.letter)
        self.letter = self.vowels[random.randint(0, 4)]
        self.string = self.string+" "+str(self.letter)
        return self.string

    def thread(self):
        self.timer = time.process_time()
        global idletrue
        idletrue = self.idletrue
        possibles()

    def evaltime(self):
        self.elapsed = time.process_time() - self.timer
        if self.elapsed > self.time:
            global idletrue
            idletrue = False
            print("time ran out (if no window appears within a few seconds, press enter)")
        
    def windowcreate(self, allinputs):
        self.user = allinputs
        del self.user[-1]
        window=tk.Tk()
        tk.Label(window, text=self.string, font="Ariel 18 italic").grid(row=3)
        string = self.string
        main.scoring(string)
        self.score = "Your score is "+ str(self.score)
        tk.Label(window, text=" ").grid(row=2, column=1)
        tk.Label(window, text=" ").grid(row=4, column=1)
        tk.Label(window, text=self.score).grid(row=5)
        tk.Label(window, text=" ").grid(row=6, column=1)
        tk.Label(window, text=self.wordlist).grid(row=7)
        tk.Label(window, text=" ").grid(row=8, column=1)
        tk.Button(window, text="HighScores", command = lambda: main.highscores()).grid(row=9)
        tk.Label(window, text="Stats:", font = "Ariel 22").grid(row=1)
        main.updatedata()
        window.mainloop()

    def updatedata(self):
        handle = sql.connect("words.db")
        cursor = handle.cursor()
        cursor.execute("INSERT INTO RESULTS VALUES(?,?,?)", (self.score, self.length, self.time))
        handle.commit()
        handle.close()

    def highscores(self):
        handle = sql.connect("words.db")
        cursor = handle.cursor()
        cursor.execute("SELECT SCORE, LENGTH, TIME FROM RESULTS")
        scores = cursor.fetchall()
        handle.commit()
        handle.close()
        print(scores)

    def scoring(self, string):
        string = list(string)
        for char in self.user:
            handle = sql.connect("words.db")
            cursor = handle.cursor()
            cursor.execute("SELECT WORD FROM WORDS")
            words = cursor.fetchall()
            handle.commit()
            handle.close()
            for word in words:
                word = str(word)
                word = word[2:len(word)-3]
                if char == word:
                    error = False
                    for letter in word:
                        try:
                            string.remove(letter)
                            string.append(letter)
                        except:
                            error = True
                    if error == False:
                        self.wordlist.append(word)
                        self.score +=1
                            
def possibles():
    thread1 = threading.Thread(target=loop_a)
    thread1.start()
    thread2 = threading.Thread(target=loop_b)
    thread2.start()  
    
def loop_a():
    while idletrue:
        main.evaltime()
            
def loop_b():
    allinputs = []
    while idletrue:
        allinputs.append(input())
    main.windowcreate(allinputs)


#load = load()
#load.loadfiles()

main = main()
main.start()


