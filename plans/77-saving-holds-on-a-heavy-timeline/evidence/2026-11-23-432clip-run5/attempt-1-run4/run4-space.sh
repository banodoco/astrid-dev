run4_space() {
  local stage="$1" required_gib="$2" free_kib
  free_kib=$(df -Pk "$BOX" | awk 'NR==2 {print $4}')
  [[ "$free_kib" =~ ^[0-9]+$ ]]
  {
    printf '%s %s free_kib=%s required_gib=%s\n' "$(date -u +%FT%TZ)" "$stage" "$free_kib" "$required_gib"
    df -h "$BOX"
  } | tee -a "$RECEIPTS/run4-disk-preflight.log"
  (( free_kib >= 5 * 1024 * 1024 && free_kib >= required_gib * 1024 * 1024 ))
}
