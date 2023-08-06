#### classFig
#### Comfortable figure handling in Python3 / Matplotlib

written by Fabolu, fabolu@posteo.de
licensed under MIT

#### Usage

from classFig.classFig import classFig # import classFig # pip install classFig

fig = classFig('PPT',(1,2)) # create figure
fig.plot([1,2,3,1,2,3,4,1,1]) # plot first data set
fig.title('First data set') # set title for subplot
fig.subplot() # set focus to next subplot/axis
fig.plot([1,2,1]) # plot second data set
fig.xlabel('Data') # create xlabel for second axis
fig.save('test.png','pdf') # save figure to png and pdf