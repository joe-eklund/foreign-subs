import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifyMovieComponent } from './modify-movie.component';

describe('ModifyMovieComponent', () => {
  let component: ModifyMovieComponent;
  let fixture: ComponentFixture<ModifyMovieComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModifyMovieComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModifyMovieComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
