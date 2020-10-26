import { NextPage } from "next";
import absoluteUrl from "next-absolute-url";

type Props = {
  success: boolean;
};
const Index: NextPage<Props> = ({ success }) => {
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: success ? "green" : "red",
        color: "white",
        fontSize: "50px",
        textAlign: "center",
        paddingTop: "25px",
      }}
    >
      {success ? "Success" : "Fail"}
    </div>
  );
};

Index.getInitialProps = async ({ req }) => {
  const { origin } = absoluteUrl(req);
  const resp = await fetch(`${origin}/api/eval`);
  const json = await resp.json();
  const success = json.success;

  return { success: success };
};

export default Index;
