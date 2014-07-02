#!/bin/bash

URL="$1"
NAME="$2"

HOSTNAME="${COLLECTD_HOSTNAME:-$(hostname -f)}"
INTERVAL="${COLLECTD_INTERVAL:-10}"



while sleep "${INTERVAL}"; do
	TIME=$(date '+%s')
	CURL_OUTPUT="PUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-time_total  ${TIME}:%{time_total}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-time_namelookup interval=${INTERVAL} ${TIME}:%{time_namelookup}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-time_connect interval=${INTERVAL} ${TIME}:%{time_connect}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-time_appconnect interval=${INTERVAL} ${TIME}:%{time_appconnect}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-time_pretransfer interval=${INTERVAL} ${TIME}:%{time_pretransfer}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-time_redirect interval=${INTERVAL} ${TIME}:%{time_redirect}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-time_starttransfer interval=${INTERVAL} ${TIME}:%{time_starttransfer}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-size_download interval=${INTERVAL} ${TIME}:%{size_download}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-size_header interval=${INTERVAL} ${TIME}:%{size_header}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-size_request interval=${INTERVAL} ${TIME}:%{size_request}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-speed_download interval=${INTERVAL} ${TIME}:%{speed_download}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-num_connects interval=${INTERVAL} ${TIME}:%{num_connects}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/gauge-num_redirects interval=${INTERVAL} ${TIME}:%{num_redirects}\nPUTVAL ${HOSTNAME}/curl_timings-${NAME}/http_response_codes-http_code_%{http_code} interval=${INTERVAL} ${TIME}:1\n"

        /usr/bin/curl -m 5 --connect-timeout 1 -s -o /dev/null -w "${CURL_OUTPUT}" -H 'Accept-Encoding: gzip,deflate' -k "${URL}"  2>/dev/null

        if [ $PPID -eq 1 ]; then
            exit 1
        fi
done

