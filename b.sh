#!/bin/bash

CMD=$1
SRC=$2

GEN_HTML=/tmp/draft.html
GEN_PREVIEW=/tmp/preview.html
RC=$(pwd)/b.rc

gen() {
  # Only generate HTML file when needed
  if [[ -f "$GEN_HTML" ]] &&  [[ $(stat -c %y "$SRC") == $(stat -c %y "$GEN_HTML") ]]; then
    return
  fi

  case "$markup" in
    mkd)
      MARKUP='markdown2 --extras=code-friendly,footnotes=^'
      ;;
    rst)
      MARKUP='my-rst2html.py'
      ;;
    *)
      echo 'Unknown markup language: $markup' >&2
      exit 1
  esac
  
  if [[ $HAS_HEADER == yes ]]; then
    $MARKUP <(sed '1,/^$/d' "$SRC") > "$GEN_HTML"
  else
    $MARKUP "$SRC" > "$GEN_HTML"
  fi

  sed "s/%%Title%%/$title/" tmpl/tmpl1.html > "$GEN_PREVIEW"
  cat "$GEN_HTML" >> "$GEN_PREVIEW"
  cat tmpl/tmpl2.html >> "$GEN_PREVIEW"

  # match the timestamp
  touch -r "$SRC" "$GEN_HTML" "$GEN_PREVIEW"
}

get_headers() {
  sed -n '1d;/^$/q;p' "$SRC"
}

insert_url() {
  if [[ $HAS_HEADER == yes ]] && get_headers | grep 'url=' >/dev/null; then
    return
  fi

  # extract the URL and insert into source of markup file
  URL=$(echo "$RESULT" | sed -n '/Post \(created\|updated\)/ s/Post \(created\|updated\): //p')
  if [[ $URL == http* ]]; then
    sed -i "1 a\\url=$URL" "$SRC"
    if [[ $HAS_HEADER == no ]]; then
      sed -i "1 a\\!b" "$SRC"
    fi
  fi
}

post() {
  if [[ $HAS_HEADER == yes ]] && get_headers | grep 'url=' >/dev/null; then
    echo "Found a url in header, about posting!" >&2
    exit 1
  fi

  RESULT=$(google blogger post --blog "$blog" --title "$title" -t "$tags" --src "$GEN_HTML" 2>&1)
  echo "$RESULT"
  insert_url
}

update() {
  if [[ ! -z $new_title ]]; then
    # need to update title
    RESULT=$(google blogger update --blog "$blog" --title "$title" \
             --new-title "$new_title" -t "$tags" --src "$GEN_HTML" 2>&1)
    if [[ $RESULT == 'Post updated*' ]]; then
      # new_title=... -> title=...
      sed -i '1,/^$/ {/^title/d}' "$SRC"
      sed -i '1,/^$/ s/^new_title/title/' "$SRC"
    fi
  else
    RESULT=$(google blogger update --blog "$blog" --title "$title" -t "$tags" --src "$GEN_HTML" 2>&1)
  fi
  echo "$RESULT"
  insert_url
}

check_header() {
  if [[ $(head -1 "$SRC") == *!b* ]]; then
    HAS_HEADER=yes
    _blog=$(get_headers | sed -n '/^blog=/ {s/^blog=//;p}')
    blog=${blog:-$_blog}
    title=$(get_headers | sed -n '/^title=/ {s/^title=//;p}')
    new_title=$(get_headers | sed -n '/^new_title=/ {s/^new_title=//;p}')
    tags=$(get_headers | sed -n '/^tags=/ {s/^tags=//;p}')
    url=$(get_headers | sed -n '/^url=/ {s/^url=//;p}')
  else
    HAS_HEADER=no
  fi
  markup=${SRC##*.}

  _title=$(basename "$SRC")
  _title="${_title%.*}"
  title=${title:-$_title}
  unset _blog _title
}

# Source configuration file, currently only for $blog
if [[ -f "$RC" ]]; then
  source "$RC"
fi

case "$CMD" in
  gen)
    check_header
    gen
    ;;
  post)
    check_header
    gen
    post
    ;;
  update)
    check_header
    gen
    update
    ;;
  *)
    echo "Unknown command: $CMD" >&2
    exit 1
    ;;
esac


