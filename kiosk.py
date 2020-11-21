from arthur import Arthur


if __name__ == '__main__':
    w = Arthur(active_artwork_path='active_artwork.jpg')
    w.start()
    w.tk.mainloop()
