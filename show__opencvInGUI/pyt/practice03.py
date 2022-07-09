import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):

        # Windowの初期設定を行う。
        super().__init__(master)
        # Windowを親要素として、frame Widget(Frame)を作成する。
        # Frameについて : https://kuroro.blog/python/P20XOidA5nh583fYRvxf/
        canvasFrame = tk.Frame(self.master)
        # Windowを親要素として、frame Widget(Frame)をどのように配置するのか?
        # packについて : https://kuroro.blog/python/UuvLfIBIEaw98BzBZ3FJ/
        canvasFrame.pack(side=tk.LEFT)
        # Windowを親要素として、frame Widget(Frame)を作成する。
        # Frameについて : https://kuroro.blog/python/P20XOidA5nh583fYRvxf/
        controlFrame = tk.Frame(self.master)
        # Windowを親要素として、frame Widget(Frame)をどのように配置するのか?
        # packについて : https://kuroro.blog/python/UuvLfIBIEaw98BzBZ3FJ/
        controlFrame.pack(side=tk.RIGHT)
        # frame Widget(Frame)を親要素として、FigureCanvasTkAggを宣言する。
        self.canvas = FigureCanvasTkAgg(fig, canvasFrame)
        # Matplotlibライブラリを利用して作成したグラフを、TkinterのWidgetとする。
        # Widgetについて : https://kuroro.blog/python/3IA9Mk6O9oBAniXsvSWU/
        tmp = self.canvas.get_tk_widget()
        # frame Widget(Frame)を親要素として、Matplotlibライブラリを利用して作成したグラフを、どのように表示するのか?
        # packについて : https://kuroro.blog/python/UuvLfIBIEaw98BzBZ3FJ/
        tmp.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # frame Widget(Frame)を親要素として、scale Widgetを作成する。
        # from_ : scale Widgetの値に下限を設定。
        # to : scale Widgetの値に上限を設定。
        # resolution : scale Widgetの値更新の大きさを設定。
        # orient : scale Widgetの表示方向を設定。水平方向。
        # command : scale Widgetの値が変更された場合に、実行する関数を設定。self.draw_plotとする。
        # Scaleについて : https://kuroro.blog/python/DUvG7YaE2i6jLwCxdPXJ/
        self.x_scale = tk.Scale(controlFrame, from_=1.0, to=10.0, resolution=0.01, orient=tk.HORIZONTAL, command=self.draw_plot)
        # frame Widget(Frame)を親要素として、scale Widgetをどのように配置するのか?
        # packについて : https://kuroro.blog/python/UuvLfIBIEaw98BzBZ3FJ/
        self.x_scale.pack(anchor=tk.NW)
        # frame Widget(Frame)を親要素として、scale Widgetを作成する。
        # from_ : scale Widgetの値に下限を設定。
        # to : scale Widgetの値に上限を設定。
        # resolution : scale Widgetの値更新の大きさを設定。
        # orient : scale Widgetの表示方向を設定。水平方向。
        # command : scale Widgetの値が変更された場合に、実行する関数を設定。self.draw_plotとする。
        # Scaleについて : https://kuroro.blog/python/DUvG7YaE2i6jLwCxdPXJ/
        self.y_scale = tk.Scale(controlFrame, from_=1.0, to=10.0, resolution=0.01, orient=tk.HORIZONTAL, command=self.draw_plot)
        # frame Widget(Frame)を親要素として、scale Widgetをどのように配置するのか?
        # packについて : https://kuroro.blog/python/UuvLfIBIEaw98BzBZ3FJ/
        self.y_scale.pack(anchor=tk.NW)
        self.draw_plot()
    # Matplotlibライブラリで作成したグラフをTkinter内で描画する。
    # リサジュー図形について : https://kagakunojikan.net/math/lissajous_figure_and_irrational_number/
    def draw_plot(self, event=None):
        # scale Widgetの値を取得する。
        v = self.x_scale.get()
        # scale Widgetの値を取得する。
        w = self.y_scale.get()
        # 0(0)~6.28(2π)までのリストを取得する。sin, cosの値を取得する。
        # 参考 : https://note.nkmk.me/python-numpy-arange-linspace/
        t = np.arange(0.0, 6.29, 0.01)
        x = np.cos(v * t)
        y = np.sin(w * t)
        # x座標の値リストを設定。
        h.set_xdata(x)
        # y座標の値リストを設定。
        h.set_ydata(y)
        # グラフを描画する。
        self.canvas.draw()

# Tkinter初学者参考 : https://docs.python.org/ja/3/library/tkinter.html#a-simple-hello-world-program
if __name__ == "__main__":
    ################################################
    # <Matplotlibの初期設定>
    # 400px x 400pxのグラフを作成する。
    # 参考 : https://analytics-note.xyz/programming/matplotlib-figsize-dpi/
    fig = Figure(figsize=(4, 4), dpi=100)
    # 1行目1列の1番目へグラフを挿入する。
    # 参考 : https://qiita.com/kenichiro_nishioka/items/8e307e164a4e0a279734#figadd_subplot
    ax = fig.add_subplot(111)
    # x軸の値の範囲を設定。
    ax.set_xlim(-1.2, 1.2)
    # y軸の値の範囲を設定。
    ax.set_ylim(-1.2, 1.2)
    # (x座標, y座標)のリスト値を元に、プロットする。
    # プロットとは? : 点をうつこと。
    # 色の設定。
    h, = ax.plot([],[], 'purple')
    ################################################

    # Windowを作成する。
    # Windowについて : https://kuroro.blog/python/116yLvTkzH2AUJj8FHLx/
    root = tk.Tk()
    app = Application(master=root)
    # Windowをループさせて、継続的にWindow表示させる。
    # mainloopについて : https://kuroro.blog/python/DmJdUb50oAhmBteRa4fi/
    app.mainloop()
    
