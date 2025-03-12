import requests
import xmltodict
import pandas as pd
import argparse
import sys

from src.fetch_research_papers.api_contants import PUBMED_API_URL, PUBMED_FETCH_URL, MAX_RESULTS


def fetch_pubmed_ids(query, max_results=MAX_RESULTS, debug=False):
    """Fetch PubMed IDs based on the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(PUBMED_API_URL, params=params)
    if debug:
        print(f"Fetching PubMed IDs for query: {query}")
        print(f"API Response: {response.json()}")
    data = response.json()
    return data["esearchresult"].get("idlist", [])


def fetch_paper_details(pubmed_id, debug=False):
    """Fetch paper details using PubMed ID."""
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    if debug:
        print(f"Fetching details for PubMed ID: {pubmed_id}")
    return xmltodict.parse(response.content)


def extract_relevant_info(xml_data, debug=False):
    """Extract required information from PubMed XML."""
    try:
        articles = xml_data["PubmedArticleSet"]["PubmedArticle"]

        # If multiple articles, take the first one
        if isinstance(articles, list):
            article = articles[0]
        else:
            article = articles

        medline_citation = article["MedlineCitation"]
        article_data = medline_citation["Article"]
        authors = article_data.get("AuthorList", {}).get("Author", [])
        title = article_data["ArticleTitle"]
        pub_date = article_data["Journal"]["JournalIssue"]["PubDate"]

        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = ""

        for author in authors:
            if "AffiliationInfo" in author:
                affiliation_info = author["AffiliationInfo"]

                # Handle case where AffiliationInfo is a list
                if isinstance(affiliation_info, list):
                    affiliations = [aff["Affiliation"] for aff in affiliation_info if "Affiliation" in aff]
                else:
                    affiliations = [affiliation_info["Affiliation"]] if "Affiliation" in affiliation_info else []

                # Filter for pharma/biotech affiliations
                for affiliation in affiliations:
                    if "pharma" in affiliation.lower() or "biotech" in affiliation.lower():
                        non_academic_authors.append(author.get("LastName", ""))
                        company_affiliations.append(affiliation)

                # Check for corresponding author email (if applicable)
                if any("Corresponding Author" in aff for aff in affiliations):
                    corresponding_author_email = author.get("Email", "")

        result = {
            "PubmedID": medline_citation["PMID"]["#text"],
            "Title": title,
            "Publication Date": f"{pub_date.get('Year', '')}-{pub_date.get('Month', '')}-{pub_date.get('Day', '')}",
            "Non-academic Authors": ", ".join(non_academic_authors),
            "Company Affiliations": ", ".join(company_affiliations),
            "Corresponding Author Email": corresponding_author_email
        }

        if debug:
            print("Extracted Information:", result)

        return result
    except Exception as e:
        print(f"Error parsing data: {e}", file=sys.stderr)
        return None


def save_to_csv(results, filename):
    """Save extracted data to a CSV file."""
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a query.")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results as CSV")

    args = parser.parse_args()

    if args.debug:
        print(f"Running with query: {args.query}")
        if args.file:
            print(f"Results will be saved to: {args.file}")
        else:
            print("Results will be printed to the console.")

    pubmed_ids = fetch_pubmed_ids(args.query, debug=args.debug)
    papers = []

    for pubmed_id in pubmed_ids:
        paper_data = fetch_paper_details(pubmed_id, debug=args.debug)
        extracted_info = extract_relevant_info(paper_data, debug=args.debug)
        if extracted_info:
            papers.append(extracted_info)
    if papers:
        if args.file:
            save_to_csv(papers, args.file)
        else:
            default_filename = f"papers_{args.query.replace(' ', '_')}.csv"
            print(f"📂 No filename provided. Saving results as: {default_filename}")
            save_to_csv(papers, default_filename)
    else:
        print("No relevant papers found.")


if __name__ == "__main__":
    main()
