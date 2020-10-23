import Head from "next/head";

function WecoApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>Rank | The relevance of search @ Wellcome Collection</title>
      </Head>
      <style jsx global>{`
        body {
          padding: 0;
          margin: 0;
        }
      `}</style>
      <Component {...pageProps} />
    </>
  );
}

export default WecoApp;
