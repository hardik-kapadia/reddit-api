from tkinter import *
from tkinter import messagebox

from reddit import reddit_api
import config as conf

root = Tk()
root.geometry("300x200")

reddit = reddit_api.get_instance_with_gfy(conf.THE_CLIENT_ID, conf.THE_CLIENT_SECRET, '<Epic:App:1.0>',
                                          conf.THE_USER, conf.THE_PASSWORD, conf.GFY_CLIENT_ID, conf.GFY_CLIENT_SECRET)
print('created an instance')


def get_data():
    print('Getting the data')
    subbr = subr.get()
    searc = search1.get()
    words = list(searc.split(" "))
    if(len(subbr) != 0 and len(words) != 0):
        print(words, "in", subbr)

        # reddit = reddit_api.get_instance_with_gfy(conf.THE_CLIENT_ID, conf.THE_CLIENT_SECRET, '<Epic:App:1.0>',
        #                                           conf.THE_USER, conf.THE_PASSWORD, conf.GFY_CLIENT_ID, conf.GFY_CLIENT_SECRET)

        # print('created an instance')

        try:
            submissions, t_count, c_count = reddit.get_posts(subbr, words, 50)
            return submissions
        except:
            print('Something went wrong')
    else:
        messagebox.showwarning("Warning", "No Data Entered")
        return None


def spam_comments():
    data = commentD.get()
    f_text = data+"\n\r\n\nThis post was made by a Bot"

    if(len(data) != 0):
        subs = get_data()
        if subs is not None:
            for sub in subs:
                sub.reply(f_text)
    else:
        messagebox.showwarning("Warning", "Enter Comment body")


lab = Label(root, text="Enter Subreddit")
subr = Entry(root)

lab1 = Label(root, text="Enter Search Terms")
search1 = Entry(root)

lab2 = Label(root, text="Enter Comment body")
commentD = Entry(root)

submit = Button(root, text="Fetch", command=get_data)
spam = Button(root, text="Comment", command=spam_comments)

lab.grid(row=0, column=0, padx=10, pady=6)
subr.grid(row=0, column=1, columnspan="4", padx=10, pady=6)

lab1.grid(row=1, column=0, padx=10, pady=6)
search1.grid(row=1, column=1, columnspan="4", padx=10, pady=6)

lab2.grid(row=3, column=0, padx=10, pady=6)
commentD.grid(row=3, column=1, columnspan="4", padx=10, pady=6)

submit.grid(row=2, column=2, padx=10, pady=10)
spam.grid(row=4, column=2, padx=10, pady=10)

root.mainloop()
