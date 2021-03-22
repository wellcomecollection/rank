import "../styles/app.css";

export default function WecoApp({ Component, pageProps }) {
  return (
    <div className="px-4 py-2 lg:max-w-3xl max-w-2xl">
      <div>
        <Component {...pageProps} />
      </div>
    </div>
  );
}
