FROM golang as builder
ADD app /
WORKDIR /
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -o /
#RUN go build .

FROM alpine
RUN apk add ca-certificates
WORKDIR /app
COPY --from=builder /TaiwanAlertBot .
CMD ["./TaiwanAlertBot"]