from tkinter import *

from reddit import reddit_api
import config as conf

root = Tk()
root.geometry("500x200")


def get_data():
    subbr = subr.get()
    searc = search1.get()
    words = list(searc.split(" "))
    print(words, "in", subbr)

    reddit = reddit_api.get_instance_with_gfy(conf.THE_CLIENT_ID, conf.THE_CLIENT_SECRET, '<Epic:App:1.0>',
                                              conf.THE_USER, conf.THE_PASSWORD, conf.GFY_CLIENT_ID, conf.GFY_CLIENT_SECRET)

    print('created an instance')

    try:
        submissions, t_count, c_count = reddit.get_posts(subbr, words, 20)
    except Error:
        print('Something went wrong')
    finally:
        print('DONE')

    


lab = Label(root, text="Enter Subreddit")
subr = Entry(root)

lab1 = Label(root, text="Enter Search Terms")
search1 = Entry(root)

submit = Button(root, text="Fetch", command=get_data)

lab.grid(row=0, column=0, padx=10, pady=6)
subr.grid(row=0, column=1, columnspan="4", padx=10, pady=6)

lab1.grid(row=1, column=0, padx=10, pady=6)
search1.grid(row=1, column=1, columnspan="4", padx=10, pady=6)

submit.grid(row=2, column=2, padx=10, pady=10)

root.mainloop()
