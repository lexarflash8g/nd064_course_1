# Start from a Debian-based image with Go installed
FROM golang:1.17

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy everything from the current directory to the PWD (Present Working Directory) inside the container
COPY . .

# Build the Go app
RUN go build -o main .

# Expose port 6111 to the outside world
EXPOSE 6111

# Run the binary program produced by `go build`
CMD ["./main"]
