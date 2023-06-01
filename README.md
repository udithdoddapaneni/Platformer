ID1110 Course Project

Platform game

1.	Introduction
a.	Objective: To make a simple 2D platform game like Mario using python.

b.	Motivation: In the beginning of the second semester we had a Game-Dev session organized by YACC, the coding club of IIT Palakkad. In that we used Godot engine which has its own language called Gdscript whose syntax is very similar to python. Using that we made an amazing platform game in less than one week. When the project was announced, the first thought that came into my (Udith) mind was this: Can such a game be made in python? So we decided to make a similar game in python


2.	Project Overview

    a.	Project goals and scope: Our initial goal was to just make a simple game that had simple features like moving left and       right, jumping, gravity and collisions and a few other features if time left. But as these things got finished quickly, we       started adding more and more features like enemies and our ambition grew. We are planning to continue this project even after     evaluation.

    b.	Project timeline: We started the project a month ago, almost immediately after the project groups were announced.  A         total of 29 commits were made (effectively 27).

        On 7th May we made our first 2 commits which relied mostly on functional programming method. But we faced a lot of               problems in the jumping and collisions part and debugging became hard as code became messy with too many constants and           variables. So we switched to object oriented method which made things a lot easier.

        On 10th May we made 5 commits that used OOP methods. On that day we added collisions, gravity, jumping with that we have         reached our initial goals. So we wanted to add more features.

        On 12th May we made 3 commits. In them we added traps that shoot fireballs upwards. And most important feature that we           added is a function that designs levels. We have divided the level into 20x14 units and one block occupies one unit. If           we give a 20x14 matrix (nested list) with integer elements as argument objects it will add objects at those locations on         the screen (the screen’s dimension is 1000x700).

        On 13th May we started coding the enemy. The objective was to make enemy move in a row (it doesn’t fall as it can float           in air). If it contacts a block it reverses its direction(Move_AI method). If the player is in its of sight, it will             shoot a fireball at the player (Vision_AI method). If the player touches it, the game ends. But we were facing some               issues in the AI part. On the same day we added Health bar and Stamina bar. The player consumes Stamina for jumping. 
        (5 commits).

        On 14th May we fixed the issues with the enemy AI. We did that by using a different algorithm and completely overhauling         the level design function. (1 commit).

        On 20th May we added two new abilities for the player : Arrow and shield. Both consume stamina and the latter has cool-           down also. We also added visual indicator in the form of text about working time of shield, cool-down time left and               whether is ON or OFF. (3 commits).

        Between 25th May to 26th May we added level management system. The game now has multiple levels and the player now spawns         at a yellow door and he has to reach green door to finish the level. Upon finishing all the levels the game ends. We also         added a main menu and win-loss messages using Tkinter. We preferred tkinter as it is best suited for tasks like adding           buttons and things like that. (3 commits)

        On 27th May we made 2 commits updating the sprites and adding visual effects for the player when the shield is ON and             OFF. 

        On 30th May we added some more levels. One of it is made by my friend Dhruvadeep (not from the team). We have highlighted         his name in the level matrix in the code as a comment. On that day we faced some glitches on Github when our teammate             Bhadra modified the readme file and sent a pull-request. Even though that request was approved the note didn’t get               modified. (4 commits, but effectively 2).

        On 31st May we added comments explaining every object and function. (1 commit).

        On 1st June we modified the code according to PEP-8 style

c.	Team Members and Contributions:
    i.	Doddapaneni Udith: Logic, code and introduction part of project report
    ii.	Vaibhav. M: Project report and main-menu
    iii.	Ramavath Bhadra: Assets

3.	Methodology
  a.	Approach and methodology employed: Object Oriented Programming

  b.	Tools, technologies, and frameworks used: Pygame, Tkinter and os modules and Microsoft paint software and online                 transparent image converting tool is used(Link mentioned in the references)


4.	Conclusion and Future Work

a.	Assessment of project success: 

So far we believe that our project was a success given the time we had for making this. But I think we still we have many things left over like adding animations.

b.	Lessons learned and recommendations for future improvements:

With the help of this project we got learn about modules like Pygame and a bit about Tkinter.  We have also learnt about the difficulty and limitations in implementing some seemingly simple but tricky tasks such as collisions and jumping. We have also learnt about some properties of image like opacities and used them to implement things like collisions with the help of masks.

But still it was a lot difficult task to do almost everything through only coding. So after the evaluation we are planning to port this game onto Godot engine to make things simpler. In Godot things like adding a following camera and animations are very easy compared to pygame where we have to code everything manually.

c.	Team Members' GitHub Accounts:

    i.	Doddapaneni Udith: https://github.com/udithdoddapaneni
    ii.	Vaibhav. M: https://github.com/vaibhzGH
    iii.	Ramavath Bhadra: https://github.com/Bhadraqueen2

6.	References:

Tutorial followed to learn about pygame: https://www.youtube.com/watch?v=jO6qQDNa2UY&t=2s

Implementation of jumping and mask collisions:
https://www.youtube.com/watch?v=B6DrRN5z_uU

Pygame documentation:
https://www.pygame.org/docs/

Tkinter documentation:
https://docs.python.org/3/library/tk.html

Transparent image converter:
https://onlinepngtools.com/create-transparent-png

