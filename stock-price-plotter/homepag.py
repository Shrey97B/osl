from tkinter import *
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from oslfetch import datfet

class FirstP(Frame):

    def __init__(self,mas):
        mas.title('Home Page')
        mas.geometry("700x600")
        mas.resizable(0,0)
        super().__init__(mas)
        self.curstsymb=''
        self.firstf  = Frame()
        self.firstf.pack()
        self.dl = Label(self.firstf,text='')
        self.dl.pack()
        self.lab1 = Label(self.firstf,text = 'Stock Price Plotter',font=('Arial',13))
        self.lab1.pack()
    		
        self.secf = Frame()
        self.secf.place(relx = 0.03,rely=0.15)
        self.templab = Label(self.secf,text='Stock Name')
        self.templab.grid(row=0,column=0)
        self.lb = Listbox(self.secf)
        self.lb.grid(row=1,column=0)
        self.dumlab = Label(self.secf,text='')
        self.dumlab.grid(row=2,column=0)
        self.lab2 = Label(self.secf,text='Select the range:')
        self.lab2.grid(row=3,column=0)
        self.var = IntVar()
        self.R1 = Radiobutton(self.secf, text="10 days", variable=self.var, value=1,command = self.setdatpric)
        self.R2 = Radiobutton(self.secf, text="6 months", variable=self.var, value=2,command = self.setdatpric)
        self.R3 = Radiobutton(self.secf, text="1 year", variable=self.var, value=3,command = self.setdatpric)
        self.var.set(1)
        self.R1.grid(row=4,column=0)
        self.R2.grid(row=5,column=0)
        self.R3.grid(row=6,column=0)
        self.v = [0,1]
        self.x = [0,1]
        self.thf = Frame()
        self.thf.place(relx=0.3,rely=0.15)
        self.fig = Figure(figsize=(6,3))
        self.a = self.fig.add_subplot(111)
        self.line1, = self.a.plot(self.v,self.x,color='red')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.thf)
        self.canvas.get_tk_widget().grid(row=1,column=0)
        self.canvas.draw()
        self.fillstocklist()
        self.lb.bind('<<ListboxSelect>>', self.changedata)
        self.fourfr = Frame()
        self.fourfr.place(relx=0.3,rely = 0.6)
        self.stnam = Label(self.fourfr,text='')
        self.stnam.grid(row=0,column=0)
        self.lastpr = Label(self.fourfr,text='')
        self.lastpr.grid(row=1,column=0)
        self.pack()
        
        
    def fillstocklist(self):
        stsymbs = ['ADANIENT','ADLABS','BATAINDIA','GILLETTE','HAVELLS','INFY','ONGC','TCS','RCOM']
        self.stname = {'ADANIENT':'Adani Enterprise','ADLABS': 'Adlabs','BATAINDIA':'Bata India','GILLETTE':'Gillette','HAVELLS':'Havells',
        'INFY':'Infosys','ONGC':'ONGC','TCS':'TCS','RCOM':'Reliance Communication'}
        for st in  stsymbs:
            self.lb.insert(END,st)
            
    def changedata(self,evt):
        widg = evt.widget
        self.curstsymb = widg.get(widg.curselection()[0])
        self.setdatpric()
        
    def setdatpric(self):
        datorig,pricdata = datfet.fetch(self.curstsymb,self.var.get())
        datstr = [str(datorig[i])[0:10] for i in range(len(datorig))]
        print(datstr)
        print(pricdata)
        temp = range(len(datstr))
        self.changeg(temp,datstr,pricdata)
        self.stnam.config(text='Stock Name: ' + str(self.stname[self.curstsymb]))
        self.lastpr.config(text='Last Price: ' + str(pricdata[len(pricdata)-1]))
        
    def changeg(self,temp,datstr,pricdata):
        print(type(datstr[0]))
        
        
        recdat = datfet.finter(self.curstsymb,datstr)
        recdat = [recdat[i][0] for i in range(len(recdat))]
        print(recdat)
        datstr2 = [str(recdat[i])[0:10] for i in range(len(recdat))]
        print(datstr)
        print(datstr2)
        
        lis = []
        
        setind = set(datstr2)
            
        for i in range(len(datstr)):
            if datstr[i] in setind:
                lis.append(i)
                
        print(lis)
        
        pricscatt = []
        for j in lis:
            pricscatt.append(pricdata[j])
            
        print(pricscatt)
        
        datstr = [datstr[i][5:10] for i in range(len(datstr))]
        
        '''
        datstr = [str(datstr[i])[5:10] for i in range(len(datstr))]
        self.line1.set_xdata(temp)
        self.line1.set_ydata(pricdata)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(0,len(temp))
        ax.set_ylim(min(pricdata)-1, max(pricdata)+1)

        ax.set_xticklabels(datstr)
        
        self.canvas.draw()
        '''
        '''
        ax = self.canvas.figure.axes[0]
        ax.set_ylim(min(pricdata)-1, max(pricdata)+1)
        ax.set_xlim(0,len(temp))
        self.a.scatter(lis,pricscatt)
        self.line1.set_xdata(temp)
        self.line1.set_ydata(pricdata)
        ax.set_xticklabels(datstr)
        self.canvas.draw()
        '''
        self.fig = Figure(figsize=(6,3))
        self.a = self.fig.add_subplot(111)
        self.line1, = self.a.plot(temp,pricdata,color='red')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.thf)    
        self.canvas.get_tk_widget().grid(row=1,column=0)
        ax = self.canvas.figure.axes[0]
        ax.set_ylim(min(pricdata)-1, max(pricdata)+1)
        ax.set_xlim(0,len(temp))
        self.a.scatter(lis,pricscatt)
        self.canvas.draw()
        
  
root = Tk()
fr = FirstP(root)
root.mainloop()

