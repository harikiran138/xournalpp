const bugIssueTemplate = (sentryErrorId) => `
### Scene content

\`\`\`
Paste scene content here
\`\`\`

### Sentry Error ID

${sentryErrorId}
`;

export default bugIssueTemplate;
