#include<iostream>
#include<fstream>
#include<cstring>
using namespace std;

class Book{
public:
    int id;
    char name[50];
    char author[50];
    int quantity;

    void input(){
        cout<<"\nEnter book id: ";
        cin>>id;
        cout<<"Enter book name: ";
        cin>>name;
        cout<<"Enter book author: ";
        cin>>author;
        cout<<"Enter book quantity: ";
        cin>>quantity;
    }

    void display(){
        cout<<"\nBook ID: "<<id;
        cout<<"\nBook Name: "<<name;
        cout<<"\nBook Author: "<<author;
        cout<<"\nBook Quantity: "<<quantity;
        cout<<"\n---------------------------";
    }
};

// ==========================
// Member Class
// ==========================
class Member{
public:
    int memberId;
    char name[50];
    char phone[20];

    void input(){
        cout<<"\nEnter Member ID: ";
        cin>>memberId;
        cout<<"Enter Member Name: ";
        cin>>name;
        cout<<"Enter Member Phone: ";
        cin>>phone;
    }

    void display(){
        cout<<"\nMember ID: "<<memberId;
        cout<<"\nName: "<<name;
        cout<<"\nPhone: "<<phone;
        cout<<"\n---------------------------";
    }
};

// ==========================
// Issue Record Class
// ==========================
class IssueRecord{
public:
    int bookId;
    int memberId;
    char issueDate[20];
    char returnDate[20];

    void display(){
        cout<<"\nBook ID: "<<bookId;
        cout<<"\nMember ID: "<<memberId;
        cout<<"\nIssue Date: "<<issueDate;
        cout<<"\nReturn Date: "<<returnDate;
        cout<<"\n-------------------------------";
    }
};

// ===============================
// Add Book
// ===============================
void addBook(){
    Book b;
    b.input();
    ofstream file("books.dat", ios::app | ios::binary);
    file.write((char*)&b, sizeof(b));
    file.close();
    cout<<"\nBook added successfully!\n";
}

// ===============================
// Display Books
// ===============================
void displayBook(){
    Book b;
    ifstream file("books.dat", ios::binary);

    if(!file){
        cout<<"\nNo record found!\n";
        return;
    }

    while(file.read((char*)&b, sizeof(b))){
        b.display();
    }
    file.close();
}

// ===============================
// Search Book
// ===============================
void searchBook(){
    int id;
    cout<<"\nEnter book ID to search: ";
    cin>>id;

    Book b;
    ifstream file("books.dat", ios::binary);

    bool found = false;
    while(file.read((char*)&b,sizeof(b))){
        if(b.id == id){
            cout<<"\nBook found:\n";
            b.display();
            found = true;
            break;
        }
    }
    if(!found){
        cout<<"\nBook not found!\n";
    }
    file.close();
}

// ===============================
// Issue Book (With Member Details)
// ===============================
void issueBook(){
    int bookId;
    cout<<"\nEnter book ID to issue: ";
    cin>>bookId;

    Book b;
    fstream file("books.dat", ios::in | ios::out | ios::binary);

    while(file.read((char*)&b, sizeof(b))){
        if(b.id == bookId){
            if(b.quantity > 0){
                b.quantity--;

                int pos = -1 * sizeof(b);
                file.seekp(pos, ios::cur);
                file.write((char*)&b, sizeof(b));

                // Enter Member Details
                Member m;
                cout<<"\nEnter Member Details:\n";
                m.input();

                // Issue Record Entry
                IssueRecord ir;
                ir.bookId = bookId;
                ir.memberId = m.memberId;

                cout<<"Enter issue date: ";
                cin>>ir.issueDate;
                strcpy(ir.returnDate, "Not Returned");

                ofstream irfile("IssueRecord.dat", ios::app | ios::binary);
                irfile.write((char*)&ir, sizeof(ir));
                irfile.close();

                cout<<"\nBook issued successfully!\n";
            }
            else{
                cout<<"\nBook out of stock!\n";
            }
            file.close();
            return;
        }
    }
    cout<<"\nBook not found!\n";
}

// ===============================
// Return Book (Update Return Date)
// ===============================
void returnBook(){
    int bookId;
    cout<<"\nEnter Book ID to return: ";
    cin>>bookId;

    Book b;
    fstream file("books.dat", ios::in | ios::out | ios::binary);

    while(file.read((char*)&b, sizeof(b))){
        if(b.id == bookId){

            b.quantity++;

            int pos = -1 * sizeof(b);
            file.seekp(pos, ios::cur);
            file.write((char*)&b, sizeof(b));

            // Update IssueRecord
            IssueRecord ir;
            fstream irfile("IssueRecord.dat", ios::in | ios::out | ios::binary);

            while(irfile.read((char*)&ir, sizeof(ir))){
                if(ir.bookId == bookId && strcmp(ir.returnDate,"Not Returned")==0){
                    cout<<"Enter return date: ";
                    cin>>ir.returnDate;

                    int pos2 = -1 * sizeof(ir);
                    irfile.seekp(pos2, ios::cur);
                    irfile.write((char*)&ir, sizeof(ir));
                    irfile.close();

                    cout<<"\nBook returned successfully!\n";
                    return;
                }
            }

            irfile.close();
        }
    }
    cout<<"\nBook not found!\n";
}

// ===============================
// Delete Book
// ===============================
void deleteBook(){
    int id;
    cout<<"\nEnter book ID to delete: ";
    cin>>id;

    Book b;
    ifstream fin("books.dat", ios::binary);
    ofstream fout("temp.dat", ios::binary);

    bool deleted = false;

    while(fin.read((char*)&b,sizeof(b))){
        if(b.id != id){
            fout.write((char*)&b, sizeof(b));
        } else {
            deleted = true;
        }
    }

    fin.close();
    fout.close();

    remove("books.dat");
    rename("temp.dat","books.dat");

    if(deleted)
        cout<<"\nBook deleted successfully!\n";
    else
        cout<<"\nBook not found!\n";
}

// =========================================================
// MAIN MENU
// =========================================================
int main(){
    int choice;

    while(true){
        cout<<"\n============= Library Management System =============";
        cout<<"\n1. Add Book";
        cout<<"\n2. Display Books";
        cout<<"\n3. Search Book";
        cout<<"\n4. Issue Book";
        cout<<"\n5. Return Book";
        cout<<"\n6. Delete Book";
        cout<<"\n7. Exit";
        cout<<"\nEnter choice: ";
        cin>>choice;

        switch(choice){
        case 1: addBook(); break;
        case 2: displayBook(); break;
        case 3: searchBook(); break;
        case 4: issueBook(); break;
        case 5: returnBook(); break;
        case 6: deleteBook(); break;
        case 7: cout<<"\nThank You!\n"; return 0;
        default: cout<<"\nInvalid choice!";
        }
    }
}