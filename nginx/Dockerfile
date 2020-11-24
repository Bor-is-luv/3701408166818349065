# Use the Nginx image
FROM nginx

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /static

# RUN mkdir /media_djumbi4
RUN mkdir /media_test_task

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/