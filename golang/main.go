package main

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"net/http"
)

func main() {
	url := "https://cdn.kernel.org/pub/linux/kernel/v6.x/ChangeLog-6.1.8"

	// HTTPリクエストを送信し、レスポンスを受け取る
	res, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer res.Body.Close()

	// HTMLドキュメントをパースする
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}

	// タイトルを取得して表示する
	title := doc.Find("title").Text()
	fmt.Println("Title:", title)
}
