FROM nanthakps/kpsml:railway
COPY . .
CMD ["bash", "start.sh"]