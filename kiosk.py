from arthur import Arthur


if __name__ == '__main__':
    w = Arthur(active_artwork_path='images/test_fake_img_1024_0_3303.jpg')
    w.start()
    w.tk.mainloop()
