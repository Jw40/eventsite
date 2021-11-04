from website import create_app

if __name__=='__main__':
    napp=create_app()
    napp.run(debug=False) #change to true to show internal server errors