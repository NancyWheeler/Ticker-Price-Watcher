import yfinance as yf
import tkinter as tk

# Create window
root = tk.Tk()
root.resizable(width=False, height=False)
root.geometry('')
root.title("Yahoo Finance")
root.configure(bg="black")
Font_tuple = ("Yahoo Sans Finance", 9, "bold")
lab = tk.Label(root)

# Create Frames
frame1 = tk.Frame(root, bg="black")
frame2 = tk.Frame(root, bg="black")
frame1.grid(row=0, column=0, sticky="n", padx=15, pady=3)
frame2.grid(row=1, column=0, sticky="s", padx=15, pady=3)

# tickers = ['BTC-USD', 'ETH-USD', 'TSLA', 'EURUSD=X', 'JPY=X', 'WISH', 'TSM', 'SNAP']
tickers = ['SPY']

# Add/remove ticker
def modTicker():
    global entry
    string = entry.get()
    if string in tickers:
        tickers.remove(string)
    else:
        tickers.append(string)
    update_ticker()
    status = tk.Label(frame2, text="Done", pady=3, padx=10, bg="black", fg="green")
    status.grid(row=0, column=1, padx=10, pady=3)

entry = tk.Entry(frame2)
entry.focus_set()
entry.grid(row=0, column=0, padx=10, pady=3)

b = tk.Button(frame2, text='Add ticker', command=modTicker)
b.grid(padx=10, pady=3)

def integer_sqrt(n): 
    x = n
    y = (x + 1) // 2
    while y < x: 
        x = y
        y = (x + n // x) // 2
    return x

# Display ticker data
def update_ticker():
    last_close = [0] * len(tickers)
    rows = integer_sqrt(len(tickers))
    columns = len(tickers) // rows
    remainder = len(tickers) % columns

    r, c, remain = 0, 0, 0

    for i in range(len(tickers)):
        ticker = tickers[i]
        
        # Create label 
        lab = tk.Label(frame1)
        lab.grid(row=r, column=c, padx=10, pady=10)
        lab.configure(font=Font_tuple, bg="black", foreground="white")

        print("\n%s" % ticker, end='')

        # Get ticker data
        try:
            data = yf.download(tickers=ticker, period='1d', interval='1m')
            close = data.iloc[-1]['Close']
        except:
            lab['text'] = "%s: N/A 🟡" % (ticker)
            lab['foreground'] = "yellow"
            continue

        # Change color based on price
        if last_close[i] > close:
            lab['text'] = "%s: %.4f 🔴" % (ticker, close)
            lab['foreground'] = "red"
        elif last_close[i] < close:
            lab['text'] = "%s: %.4f 🟢" % (ticker, close)
            lab['foreground'] = "green"
        else:
            lab['text'] = "%s: %.4f ⚪" % (ticker, close)

        last_close[i] = close
        
        # Place the labels into grid
        if c == columns and r == rows and remain <= remainder:
            r+=1
            c=0
            remain+=1
        elif c == columns:
            c=0
            r+=1
        else:
            c+=1       

    root.after(60000, update_ticker)

update_ticker()

root.mainloop()