# Blog: Similar Clothes Search

**Dovydas Baranauskas**

## My First Blog Entry 04/11/2018

This is my first blog entry.

This week I completed the [Fastai](https://www.fast.ai/) course on Deep Learning. I made a quick draft of the web application using flask. It was my first flask web application so I made a quick application with a button and basic HTML as a mock design with no functionality.
I also started working on my machine learning pipeline. I got the tensorflow-keras framework to work with my GPU by setting up CUDA drivers. I started work on my functional specification also, I began by creating user stories, the operational scenarios, and the constraints. 

Overall the week was fairly productive, I did a lot of set up work for my project and I can start some development next week. 
For the next 2 week sprint I hope to: 
Implement user file uploads to the server and display them
Start my machine learning pipeline by implementing some basic NN classifiers.

## My Second Sprint Blog Entry 19/11/2018

The last 2 week sprint had a few ups and downs. I implemented the functionality for users to upload files to the web server. But there was a problem displaying them, which I decided to put off until next week as I wanted to get my machine learning pipeline started. I installed anaconda and decided to get going by using Jupyter notebooks. I wanted to follow the tutorial for an categorical classifier using the Deep Fashion dataset described [here](https://medium.com/deep-learning-turkey/deep-learning-lab-episode-4-deep-fashion-2df9e15a63e1). After I got everything set up, anaconda navigator stopped functioning, and I could not run code correctly. After trying to debug for a couple of days, I gave up as there was compatibility issues, and decided to try using Google Colab, which offer a free GPU in a Jupyter like interface. It was fairly easy to set up following this tutorial [here](https://medium.com/deep-learning-turkey/google-colab-free-gpu-tutorial-e113627b9f5d). After I set everything up and ran the code, I realised that data pre-processing was taken a very long time as google drive takes a very long time to unzip and process all the image files which were stored on google drive. 
<br/>
So instead, I decided to install Ubuntu on my pc and try run to see if it runs better on a Linux distribution. After setting up Ubuntu and running code in Jupyter notebook I realised that for some reason the OS was not performing correctly and would consistently get out of memory errors. So I finally decided to reinstall my windows OS and reinstall anaconda. After finally reinstalling windows, I tried running anaconda and everything worked, so I assume there was something originally wrong in the windows operating system I had installed.

I also worked on my functional specification over the week, I am on the final parts where I need to add the high level design, and the preliminary schedule. I finished off the week by adding a login and register function to my web application. 

For the next sprint I will hope to implement:
User login and uploading images and see the images that they have uploaded 
Set up user profiles
Add feedback from user action
Finish off the functional Specification

As the semester is coming to a close soon, and I am very busy with assignments and study for exams, the next sprint will last 4 weeks.

## My Third Sprint Blog Entry 23/12/2018

With the end of semester and exam season looming, there was little time to work on my project over the last 4 weeks. I started off by fixing the problem I was having with user uploading files displaying. When a user uploads a file, they will see the image they uploaded and will eventually be able to see all the images returned by the algorithm when it is up and running. A quick screenshot here shows how the user would see it.
<br/>![queryImage](https://gitlab.computing.dcu.ie/baranad2/2019-ca400-baranad2/raw/master/docs/blog/images/queryImage.png)<br/>

I also got the user profile page up and running so now any user can view their profile and see how many images they have uploaded. This is done with a SQLite database that maps users to each image that they have uploaded. An example output is shown here:
<br/>![UserImage](https://gitlab.computing.dcu.ie/baranad2/2019-ca400-baranad2/raw/master/docs/blog/images/userprofile.png)<br/>

I also tried to fix some issues that myself and my supervisor discussed in our meeting. 
We found a bug that would cause the registration page to crash due to not being logged in correctly, this was fixed.
We decided to add a gitignore file to ignore the pyc, .idea, and we ignore any image file that was uploaded to the server.
We decided to add a bit more information on the splash page for the user about our web application.
The folder hierarchy got muddled up while I was coding so I simplified it by removing some folders so it would be easier to read and access.
I also fixed filename vulnerability which could have allowed users to upload file with names such as../../home.png to put files on our servers.
And finally users can no longer attempt to upload files which are not png,jpeg, or jpg. If they do, they will get this error message:
<br/>
![UploadImage](https://gitlab.computing.dcu.ie/baranad2/2019-ca400-baranad2/raw/master/docs/blog/images/fileUploadError.png)<br/>
I will take a break from the project until after the exams are over as I want to focus on studying. After the exams, I will meet up with my supervisor, and hope to get the machine learning pipeline operational as soon as possible.

## My Fourth Sprint Blog Entry 23/01/2019
After the exam break, I quickly went back to working on the project. The main goal was to iron out some bugs that were still present in the application, add some more informative logging, add unit testing, and deploy the web application on a production server.
I started by adding more informative logging using flask logging package. We can get useful logging information such as
-Users logging in to the app
-Newly created users
-Users logging out, etc.
I then added unit tests to the flask application using pytest. I added a test database with a simple test user and a basic configuration for the tests in the conftest file.
Then in the test_app.py I have all of the test cases for testing the basic features of the web app. There are test cases for checking if users can login and logout, if users can register, if logged in user can access all the correct pages, and if none logged in users get redirected properly and test general access to the web app.
Finally I added the web application on to a production server using Digital Ocean. The application is served using uWSGI and Nginx. I set up uWSGI to server the web application whenever the server reboots. Once uWSGI was up and running, I used Nginx to pass web requests to the socket using the uWSGI protocol. Finally I wanted to get a SSL certificate to secure my web app. 
```
sudo certbot --nginx -d simsearch.ml -d www.simsearch.ml
```
This runs certbot with the --nginx plugin, using -d to specify the name we'd like the certificate to be valid for. It ran successfully and I was able to have SSL certificate for the simsearch.ml domain where the web app will be hosted.

For the next sprint I hope to
Add new error pages
Replace locally stored image files with AWS buckets

## My Fifth Sprint Blog Entry 04/02/2019
I started this week by adding new 404 and 500 error pages. This will allow users to access a back button feature or any feature from the menu, when they encounter an error, which allows for easy reversal of action. 
I also removed a vulnerability that allowed users to upload files for other users. Now a user will be redirected if trying to access another user’s page.
The main goal for this week was to replace the image files that were stored in a static folder on the server and use amazon's S3 to host the image folder. Using the boto3 flask API I was able to set up integration with the AWS bucket and the flask application.
When a user uploads a file, it now gets uploaded to the AWS bucket, in a folder that has the user’s username. Any file the user has uploaded gets printed in the profile tab.
I also added a feature to remove and file a user may not want to see anymore. All the links are also pre-signed with an expiration date. This will protect the user’s data in case information gets shared.
I also added new test cases to test the integration with the AWS bucket, and the new delete function.
Finally I also added selenium front end testing with a chrome web driver, so that I would be able to also see the front end of my application when running tests so that I can analyse if it performing correctly. This test follows all the possible interactions with the web application.
The test is shown below!

![Gif of selenium front end test](https://media.giphy.com/media/nEDQZPjGo49P7I72dM/giphy.gif)
<br/>
For the next sprint, I hope to star my machine learning part of my project. I will need to do some more research on neural networks and their implementation.

## My Sixth Sprint Blog Entry 18/02/2019
I have starting the machine learning portion of the project over the last 2 weeks. I started out by setting up a Google Cloud Platform instance with a GPU so that I could start training and experimenting with neural networks using the Fastai library. I set up the fast AI library, and began following the new updated tutorial on fast.ai. I followed the 3 tutorials on classification with neural networks which gave me an in depth practical understanding of neural networks.
I had a meeting with my supervisor the following week, and he sent me the data from the Deep Fashion dataset. He had cleaned it up so that it was labelled consistently, and loaded into a fast AI classifier with 50% accuracy. Over the next few days I experimented with the data and achieved a 69% accuracy for the classifier. I then attempted to implement a bounding box classifier with the Fastai library but it turns out the library is not yet set up for this task. So I began investigating object classification in PyTorch. At this time I also began the application process for a graduate position at Amazon Web Services.

I am not too sure about the plan for the next sprint. If I get through to the next round of online assessments for AWS, I will focus on this. Otherwise, I will hope to continue my machine learning research and implementation of the prediction model. 

## My Seventh Sprint Blog Entry 09/03/2019
Over the next two weeks I decided to put my project work on hold as the majority of my extra time was taken by studying for the online assessments for my job application at AWS. I then had an interview which I needed to study for also. Fortunately I received an offer for the position so all the time I could not work on the project was not in vain!

Since my application was successful I am now free to focus on my project. For the next sprint, the main objective was to implement a clothes similarity search model, and begin training.

## My Eighth Sprint Blog Entry 29/03/2019
Over the last 3 weeks I focused on training a deep learning model to recognise similarity in clothes. I based my implementation off of the [Deep Image similarity paper](http://users.eecs.northwestern.edu/~jwa368/pdfs/deep_ranking.pdf), and following [this](https://github.com/SathwikTejaswi/deep-image-similarity-ranking) implementation on GitHub that used a more simple approach that replaced the multi scale neural network with a resnet model, and uses the built in PyTorch triple loss function. The GitHub implementation used the tiny dataset. I replaced the data set with the deep fashion in shop retrieval dataset and modified the model to fit my dataset. I studied how to initialise neural networks with PyTorch and how to apply the PyTorch [Triple Loss Fucntion](https://pytorch.org/docs/0.3.1/nn.html?highlight=tripletmarginloss). 
<br/>
I first needed to clean up all the text annotation files and make them csv files to allow me to access them as panda’s data frames. I needed to change -1's into 0s so that all values are uniform throughout the dataset and do other clean up tasks. The python notebook for this task is called fixup in the repository.
After this, I needed to set up the data set to create an in class positive image, in class negative image, and an out class image. The in class positive image is the same image in a different pose if that image exists. The in class negative image is an image in the same category as the query image, for example if the query image was a dress, any other dress from the class that is not the same dress will be considered as an out class negative. Finally the out class image is any randomly chosen image that is not in the same category as the query image. For example, if the query image was a dress, the outclass image would be a tank-top. An example of these images are shown below:
<br/>
![UploadImage](https://gitlab.computing.dcu.ie/baranad2/2019-ca400-baranad2/raw/master/docs/blog/images/anchors.PNG)
<br/>
I also needed to set up a data loader class to read in data for the model. I set it up to be similar to the tiny dataset example from the GitHub repository. Once I set this up and initialised the model, it was time to train the model. I started with 6 epochs, which yielded about a .30 triplet loss. I did not know if this was low enough or not so I decided to keep going with the implementation and test the results. I then encoding images into embedding vectors to facilitate the image search. After this I got results that were not very accurate. So I decided to train for another 6 epochs, and the results were slowly improving. But after I trained the network, I went to shut down the google cloud instance, and by mistake pressed the delete button and not the shutdown button. This deleted all of the files on the VM instance. Luckily I had backed up the 2 python notebooks 2 days prior. I needed to re-download all the image files and set up the VM. This took up about 3 days to get back to where I was. I had to retrain the model. I started with 40 epochs and these were the results that I got.
<br/>
![UploadImage](https://gitlab.computing.dcu.ie/baranad2/2019-ca400-baranad2/raw/master/docs/blog/images/Results.PNG)
<br/>
I then decided to train for 40 more epochs in hopes that it would improve accuracy further. The loss went down to about 0.17. Looking at the results of the model, it seemed like the model was focusing on the whole picture instead of the actual clothing. While it did have some good results, some results were very far off. I concluded this to be due to analysing the entire picture rather than the single article of clothing as I was not using bounding boxes, I will address this when I go back to retrain the model, as for the next sprint, I want to focus on deploying the model in the web application.

## My Ninth Sprint Blog Entry 04/04/2019
Over the last week, I began implementing my model to integrate with my flask application. I needed to take in the uploaded query image and process it, and send back similar images to the user. This was done in 2 separate files. 1 file created the data class that would take in the image and apply the correct transformations and load it to be read by the model, and a second file to initialise the class and transform the image into an embedding and get similar images back. The results of uploading an image are shown below.
<br/>
I also decided to add a feature to allow users to search previously uploaded images. A users can click the search button beside the image, and this will redirect users and search for the same image again giving you the results. I also added a loading gif to show users that their data is being processed while the model is creating the embedding’s. For the next sprint I hope to move the changes to the live server from local host.

## My Tenth Sprint Blog Entry 17/04/2019
After integrating the model with the flask application, I began to push the changes to the server. There were many problems as I had to migrate some files to the server that were missing. I had problems installing Pytorch for CPU as the server does not have a GPU. Once I resolved the installation issues, I was having another problem as the website was running out of RAM. I had to increase the RAM in my digital ocean droplet, but this only allows 1 or 2 runs before the website crashes. But everything was up and running so I was happy with that.
I had a meeting with my supervisor, and we were both not impressed with the accuracy of the model, so we decided to that I should try crop the images around the bounding boxes to improve the accuracy. I implemented this change and retested the model, the results were a bit better but still not great. The results are shown below:
<br/>
![images](https://gitlab.computing.dcu.ie/baranad2/2019-ca400-baranad2/raw/master/docs/blog/images/new_results.png)
<br/>
After this change I also began working on my documentation, creating my user and technical manuals. I also began fixing the test cases that were failing due to the addition of the ML algorithm, made sure the code met flake8 standards again, fixed a bug with deleting files, and I also added new test cases to account for new features. 
I started carrying out user testing, and of the users informed me that I should add a way to delete user profiles to meet GDPR standards. I then went on to add this feature so now a user can click the delete profile button to remove all uploaded images and delete the account. I also went on to add a feature to allow users to rate the result that they got returned. This way I can have a “Human in the Loop” to help steer the model to more accurate results as I can pull down all the images that are marked as positive or negative. The UI for this is shown below.
<br/>
![images](https://gitlab.computing.dcu.ie/baranad2/2019-ca400-baranad2/raw/master/docs/blog/images/rating.png)
<br/>
For the next sprint I will be focusing on the user and technical manuals as I am begging my study for the final exams

## My Eleventh Sprint Blog Entry 18/05/2019
There were four days before the deadline for the final year project after our final exams. I took the Thursday and Friday to finish off my technical manual. I had a meeting with my supervisor and we decided that there was no point to add any extra features in case there would be unoforseen bugs for the demonstartion. I had the technical document finished by Friday night, and the video walkthrough on Saturday. On Sunday I will make my demo presentation, and practice for it. 









