# History of Databases: Why Were They Invented?

**Source:** https://www.cockroachlabs.com/blog/history-of-databases-distributed-sql/

## Before Computers (Pre-1960s)

Data was stored in physical filing cabinets - journals, libraries, filing systems for:
- Health records
- Tax papers
- Important documents

**Problems:**
- Took up physical space
- Difficult to find information
- Hard to back up
- No way to answer complex questions across documents

## The Birth of Computer Databases (1960s)

First database management systems (DBMS) emerged as computing power increased and prices decreased.

**Early Systems:**
- Navigational databases (hierarchical and network models)
- Required users to navigate through entire database to find information
- IBM's Information Management System (IMS)
- Charles Bachman's Integrated Data Store (IDS)

## The Revolutionary Moment: E.F. Codd's Relational Model (1970)

**Paper:** "A Relational Model of Data for Large Shared Data Banks" (June 1970)

**Key Innovation:** Building cross-linked tables that allow you to store any piece of data **just once**

**Business Problems Solved:**

1. **Efficient Storage**
   - Disk space was expensive in the 1960s-70s
   - Relational model reduced redundancy
   - Store each fact only once

2. **Flexible Querying**
   - Database could answer **any question**, so long as the answer was stored somewhere in it
   - No need to know the question in advance
   - No need to design navigation paths

3. **Schema Independence**
   - Database's logical organization (schema) disconnected from physical storage
   - This became the standard principle for database systems

**Original Objectives:** Address "each and every one of the shortcomings that plagued those systems that existed at the end of the 1960s decade"

## The Relational Era (1970s-1990s)

- **1979:** Oracle - first commercial relational database
- **1980s-90s:** Relational databases became dominant
- Network and hierarchical models declined
- **SQL** (Structured Query Language) became the standard language of data

**Key Features Introduced:**
- Rich indexes
- Table joins
- Transactions
- Standardized query language

## Why This Matters for Students

When you're learning SQL and working with DuckDB, you're using a technology born from a fundamental business need: **how do we store information once and answer any question about it?**

This is why understanding tables, keys, and relationships is so important - it's the foundation that solved one of computing's biggest early problems.
