import Header from "@/components/Commons/Header";
import FeatureCard from "@/components/Commons/FeatureCard";
import Footer from "@/components/Commons/Footer";
import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <>
      <div className="hero">
        <video autoPlay muted loop className="background-video">
          <source src="/bg3.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="hero-content">
          <h2 className="hero-heading">
            <span>
              Empower your
              <span className="hero__boring-text"> marketing efforts</span>
            </span>
            <span>
              with
              <span className="hero__gradient-text">&nbsp;AdWise.ai</span>
            </span>
          </h2>
          <p className="hero__description">
            Upload your product details or documents, and let Adwise.AI provide
            market analysis and ad content tailored to the latest trends. Your
            gateway to smarter advertising.
          </p>
          <div className="buttons">
            <a href="#features" className="btn-secondary">
              Discover Features
            </a>
            <Link to="/create" className="btn-primary">
              Get Started
            </Link>
          </div>
        </div>
      </div>
      <main className="homepage">
        <section id="features" className="features">
          <h2 className="t">Powerful Features</h2>
          <div className="features-container">
            <div className="features-grid">
              <FeatureCard
                title="Product Insights"
                description="Analyze your product’s market position and discover actionable insights to boost its appeal. Let Adwise.AI be your data-driven guide to smarter marketing decisions."
              />
              <FeatureCard
                title="Trend-Based Content"
                description="Generate ad content aligned with the latest market trends. Stay relevant and captivating, ensuring your campaigns resonate with your audience."
              />
              <FeatureCard
                title="Comprehensive Reports"
                description="Receive detailed market analysis and performance projections, helping you strategize effectively and maximize your ROI."
              />
            </div>
          </div>
        </section>
        <section id="about" className="about">
          <div className="container">
            <h2 className="t">About Adwise.AI</h2>
            <p>
              Struggling to craft compelling ads or identify the best strategies
              for your product? Adwise.AI is here to revolutionize your
              advertising journey. Our OaaS (Optimization-as-a-Service) platform
              simplifies the process by taking your product details or documents
              and performing a thorough market analysis. Adwise.AI then
              generates ad content tailored to current market trends, ensuring
              your campaigns stay ahead of the competition. Say goodbye to
              guesswork and hello to smarter, data-driven advertising.
            </p>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}

export default Home;
