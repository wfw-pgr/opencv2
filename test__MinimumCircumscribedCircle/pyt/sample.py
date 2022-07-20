# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys


def getCircle(frame, lower_color, upper_color):
    
  MIN_RADIUS = 25

  # HSVによる画像情報に変換
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  # ガウシアンぼかしを適用して、認識精度を上げる
  blur = cv2.GaussianBlur(hsv, (9, 9), 0)

  # 指定した色範囲のみを抽出する
  color = cv2.inRange(blur, lower_color, upper_color)

  # オープニング・クロージングによるノイズ除去
  element8 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)
  oc = cv2.morphologyEx(color, cv2.MORPH_OPEN, element8)
  oc = cv2.morphologyEx(oc, cv2.MORPH_CLOSE, element8)

  # 輪郭抽出
  ret = cv2.findContours(oc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contours, hierarchy = cv2.findContours(oc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # print( ret )
  # print( type(ret) )
  # print( type( contours1 ), type( hierarchy1 ) )
  # sys.exit()
  # img, contours, hierarchy = cv2.findContours(oc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  print("{} contours.".format(len(contours)))

  if len(contours) > 0:
    # 一番大きい赤色領域を指定する
    contours = list( contours )
    contours.sort(key=cv2.contourArea, reverse=True)
    cnt = contours[0]

    # 最小外接円を用いて円を検出する
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)

    # 円が小さすぎたら円を検出していないとみなす
    if radius < MIN_RADIUS:
      return None
    else:
      return center, radius
  else:
    return None


if __name__ == '__main__':
  # 内蔵カメラを起動(カメラが一つしか繋がっていない場合は、引数に0を渡せば良い)
  # cap = cv2.VideoCapture(0)

  # while True:
    # 赤色の円を抽出する
    # frame = cap.read()[1]
    frame    = cv2.imread( "jpg/red_ball.png" )
    getframe = getCircle( frame, np.array([130, 80, 80]), np.array([200, 255, 255]))

    # if getframe is not None:
      # 見つかった円の上に青い円を描画
      # getframe[0]:中心座標、getframe[1]:半径
    cv2.circle(frame, getframe[0], getframe[1], (255, 0, 0), 2)
    print(getframe[1])

    # 検出結果とともに映像を表示
    cv2.imshow('Circle Detect', frame)


  # # 終了時にカメラを解放
  # cap.release()
  # cv2.destroyAllWindows()
