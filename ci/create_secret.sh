cat <<'EOL' > .lamvery.secret.yml
key_id: {{ env['AWS_KMS_KEY_ID'] }}
cipher_texts: {}
EOL

ruby -e'(ENV.select {|env| env =~ /^LAM_SECRET_*/}).each_pair {|k,v| system("lamvery encrypt -n #{k[11..-1].downcase} #{v} -s")}'
