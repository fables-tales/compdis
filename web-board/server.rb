require "sinatra"

get "/" do
    open("html/index.html").read()
end
