import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Type Safe & Robust',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Fully typed with <code>Python 3.10+</code> and <code>Pydantic v2</code>.
        <br />
        Catch errors before runtime with robust validation and intelligent IDE autocompletion.
      </>
    ),
  },
  {
    title: 'Modern Async API',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Designed for the modern web. Built-in <strong>Async</strong> support and SSE streaming capabilities for high-concurrency applications.
      </>
    ),
  },
  {
    title: 'Feature Rich',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Complete support for NovelAI features: Text Generation, Image Generation (V4/Anime V3), Vibe Transfer, and advanced image handling with Pillow.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="card-premium">
        <div className="text--center">
          <Svg className="featureSvg" role="img" />
        </div>
        <div className="card-content text--center">
          <Heading as="h3">{title}</Heading>
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
