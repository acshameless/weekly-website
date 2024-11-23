import rss from "@astrojs/rss";

export function GET() {
  let allPosts = import.meta.glob("./posts/*.md", { eager: true });
  let posts = Object.values(allPosts);

  posts = posts.sort((a, b) => {
    const getPostNumber = (url) =>
      parseInt(url.split("/posts/")[1].split("-")[0]);
    return getPostNumber(b.url) - getPostNumber(a.url);
  });

  // Only 12 are kept
  posts = posts.slice(0, 12);

  return rss({
    title: "Weekly Report",
    description: "记录工程师 shameless 的 weekly report",
    site: "https://weekly.shameless.top/",
    customData: `<image><url></url>https://aea62e6.webp.li/2024/11/favicon.png</image>`,
    items: posts.map((item) => {
      const [issueNumber, issueTitle] = item.url.split("/posts/")[1].split("-");
      const title = `第${issueNumber}周 - ${issueTitle}`;
      return {
        link: item.url,
        title,
        description: item.compiledContent(),
        pubDate: item.frontmatter.date,
      };
    }),
  });
}
